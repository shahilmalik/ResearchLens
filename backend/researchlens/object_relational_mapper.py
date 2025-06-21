from django.db import connection
from .models import Paper, Author
import json
import numpy as np


class PaperMapper:
    """This class is responsible for mapping the Paper model to the database and providing methods to fetch, create, and update papers from the database."""
    
    def __init__(self):
        self.paper_table_name = 'researchlens_paper'
        self.author_table_name = 'researchlens_author'
        self.paper_authors_table_name = 'researchlens_paper_authors'
    
    def get_filtered(self, **kwargs):
        """Fetch all papers from the database ordered by publication date and filtered by the provided filtering elements."""
        
        # Initialize the where clause filters
        filters = []
        filter_params = []
        
        # Apply filters based on kwargs by appending it to the WHERE clause
        for key, value in kwargs.items():
            if key == 'embedding':
                filters.append("p.embedding is %s")
                filter_params.append(value)
            elif key == 'keywords':
                filters.append("p.keywords = %s")
                filter_params.append(value)
        
        with connection.cursor() as cursor:
            # Build the query with filters
            query = (
                "SELECT p.id, p.arxiv_id, p.title, p.abstract, p.keywords, p.published_date, p.link, p.categories, "
                "a.id, a.name, a.institution "
                "FROM researchlens_paper p "
                "INNER JOIN researchlens_paper_authors pa ON p.id = pa.paper_id "
                "INNER JOIN researchlens_author a ON pa.author_id = a.id "
                f"{'WHERE ' + ' AND '.join(filters) if filters else ''} "
                "ORDER BY p.published_date DESC;"
            )
            
            # Execute the query with parameters
            cursor.execute(query, filter_params)
            
            # Fetch all rows and construct Paper and Author objects
            papers = {}
            rows = cursor.fetchall()
            for row in rows:
                paper_id = row[0]
                
                # Create a new Paper object if it doesn't exist
                if paper_id not in papers:
                    paper = Paper(
                        id=row[0],
                        arxiv_id=row[1],
                        title=row[2].replace('\n', ' ').replace('\r', ' ').strip(),
                        abstract=row[3].replace('\n', ' ').replace('\r', ' ').strip(),
                        keywords=json.loads(row[4]) if row[4] else [],
                        published_date=row[5],
                        link=row[6],
                        categories=row[7]
                    )
                    paper.authors = []
                    papers[paper_id] = paper
                
                # Create a new Author object
                author = Author(
                    id=row[8],
                    name=row[9],
                    institution=row[10]
                )
                
                # Avoid duplicate authors
                if author not in papers[paper_id].authors:
                    papers[paper_id].authors.append(author)
        
        return list(papers.values())
    
    def get_excluded(self, **kwargs):
        """Fetch all papers from the database ordered by publication date and that excludes paper that matches the given criterion."""
        
        # Initialize the where clause filters
        filters = []
        filter_params = []
        
        # Apply filters based on kwargs by appending it to the WHERE clause
        for key, value in kwargs.items():
            if key == 'embedding':
                filters.append("p.embedding is not %s")
                filter_params.append(value)
        
        with connection.cursor() as cursor:
            # Build the query with filters
            query = (
                "SELECT p.id, p.arxiv_id, p.title, p.abstract, p.keywords, p.published_date, p.link, p.categories, p.embedding,"
                "a.id, a.name, a.institution "
                "FROM researchlens_paper p "
                "INNER JOIN researchlens_paper_authors pa ON p.id = pa.paper_id "
                "INNER JOIN researchlens_author a ON pa.author_id = a.id "
                f"{'WHERE ' + ' AND '.join(filters) if filters else ''} "
                "ORDER BY p.published_date DESC;"
            )
            
            # Execute the query with parameters
            cursor.execute(query, filter_params)
            
            # Fetch all rows and construct Paper and Author objects
            papers = {}
            rows = cursor.fetchall()
            for row in rows:
                paper_id = row[0]
                
                # Create a new Paper object if it doesn't exist
                if paper_id not in papers:
                    paper = Paper(
                        id=row[0],
                        arxiv_id=row[1],
                        title=row[2].replace('\n', ' ').replace('\r', ' ').strip(),
                        abstract=row[3].replace('\n', ' ').replace('\r', ' ').strip(),
                        keywords=json.loads(row[4]) if row[4] else [],
                        published_date=row[5],
                        link=row[6],
                        categories=row[7],
                        embedding=json.loads(row[8]) if row[8] is not None else None
                    )
                    paper.authors = []
                    papers[paper_id] = paper
                
                # Create a new Author object
                author = Author(
                    id=row[9],
                    name=row[10],
                    institution=row[11]
                )
                
                # Avoid duplicate authors
                if author not in papers[paper_id].authors:
                    papers[paper_id].authors.append(author)
        
        return list(papers.values())
        
    def get(self, page=1, page_size=10, search="", start_date=None, end_date=None, categories=None):
        """Fetch a page with papers and their authors from the database ordered by publication date and filtered
        by the provided filtering elements. The function supports pagination for lazy loading of the papers."""
        
        papers = {}
        with connection.cursor() as cursor:
            # Intialize the where clause filters
            filters = []
            filter_params = []
            
            # Apply filters based on search, start_date, end_date, and categories by appending it to the WHERE clause
            if search != "":
                filters.append("to_tsvector('english', p.title || ' ' || p.abstract || ' ' || a.name) @@ plainto_tsquery('english', %s)")
                filter_params.append(search)
            if start_date:
                filters.append("p.published_date >= %s")
                filter_params.append(start_date)
            if end_date:
                filters.append("p.published_date <= %s")
                filter_params.append(end_date)
            if categories:
                categories_list = categories.split(',')
                placeholders = ', '.join(['%s'] * len(categories_list))
                filters.append(f"p.categories IN ({placeholders})")
                filter_params.extend(categories_list)
            
            if filters:
                # Query to get the all relevant paper ids. This is needed to count the total number of papers and for
                # the pagination. One single query for the pagination with LIMIT and OFFSET is not possible here because
                # we get author-paper pairs and not only papers. Thus, LIMIT and OFFSET would not work correctly and return
                # to little papers (because one paper can have multiple authors).
                count_query = (
                    "SELECT DISTINCT(p.id), p.published_date "
                    "FROM researchlens_paper p "
                    "INNER JOIN researchlens_paper_authors pa ON p.id = pa.paper_id "
                    "INNER JOIN researchlens_author a ON pa.author_id = a.id "
                    "WHERE " + " AND ".join(filters) + "ORDER BY p.published_date DESC;"
                )
            else:
                # Same as aboive, but without any filters
                count_query = (
                    "SELECT DISTINCT(p.id), p.published_date "
                    "FROM researchlens_paper p "
                    "INNER JOIN researchlens_paper_authors pa ON p.id = pa.paper_id "
                    "INNER JOIN researchlens_author a ON pa.author_id = a.id "
                    "ORDER BY p.published_date DESC;"
                )
            
            # Execute the count query to get the total number of papers
            count_params = tuple(filter_params)
            cursor.execute(count_query, count_params)
            ids = [r[0] for r in cursor.fetchall()]
            total_count = len(ids)
            
            if total_count == 0:
                return 0, []
            
            # Apply pagination
            page_ids = ids[(page - 1) * page_size: page * page_size]
            print(page_ids)
            
            # Execute the query with parameters
            # Fetch papers and their authors in a single query from the database.
            # This assumes a many-to-many relationship between papers and authors.
            query = ("SELECT p.id, p.arxiv_id, p.title, p.abstract, p.keywords, p.published_date, p.link, p.categories, "
                "a.id, a.name, a.institution "
                "FROM researchlens_paper p "
                "INNER JOIN researchlens_paper_authors pa ON p.id = pa.paper_id "
                "INNER JOIN researchlens_author a ON pa.author_id = a.id "
                f"WHERE p.id IN ({', '.join(['%s'] * len(page_ids))}) "  # Use IN clause for pagination
                "ORDER BY p.published_date DESC ")
            cursor.execute(query, page_ids)
            
            
            # Fetch all rows and construct Paper and Author objects
            rows = cursor.fetchall()
            for row in rows:
                paper_id = row[0]
                
                # Create a new Paper object if it doesn't exist
                if paper_id not in papers:
                    paper = Paper(
                        id=row[0],
                        arxiv_id=row[1],
                        title=row[2].replace('\n', ' ').replace('\r', ' ').strip(),
                        abstract=row[3].replace('\n', ' ').replace('\r', ' ').strip(),
                        keywords=json.loads(row[4]) if row[4] else [],
                        published_date=row[5],
                        link=row[6],
                        categories=row[7]
                    )
                    paper.authors = []
                    papers[paper_id] = paper
                
                # Create a new Author object
                author = Author(
                    id=row[8],
                    name=row[9],
                    institution=row[10]
                )
                
                # Avoid duplicate authors
                if author not in papers[paper_id].authors:
                    papers[paper_id].authors.append(author)
                    
        return total_count, list(papers.values())
    
    def get_by_arxiv_id(self, arxiv_id):
        """Fetch a paper by its ID and return it."""
        
        with connection.cursor() as cursor:
            # Query to get the paper and its authors
            query = ("SELECT p.id, p.arxiv_id, p.title, p.abstract, p.keywords, p.published_date, p.link, p.categories "
                "FROM researchlens_paper p "
                "WHERE p.arxiv_id = %s")
            cursor.execute(query, [arxiv_id])
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Fetch all rows and construct Paper and Author objects
            paper = Paper(
                id=row[0],
                arxiv_id=row[1],
                title=row[2].replace('\n', ' ').replace('\r', ' ').strip(),
                abstract=row[3].replace('\n', ' ').replace('\r', ' ').strip(),
                keywords=json.loads(row[4]) if row[4] else [],
                published_date=row[5],
                link=row[6],
                categories=row[7]
            )
            paper.authors = []
            
        return paper
    
    def get_or_create(self, arxiv_id, defaults):
        """Get or create a paper by arxiv_id. If the paper does not exist, it will be created with the given parameters."""
        
        # Check if the paper already exists
        paper = self.get_by_arxiv_id(arxiv_id)
        if paper:
           return paper, False
            
        with connection.cursor() as cursor:
            # If not found, create a new paper by inserting it into the database
            cursor.execute(
                "INSERT INTO researchlens_paper (arxiv_id, title, abstract, published_date, categories, keywords, link)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (arxiv_id, defaults["title"], defaults["abstract"], defaults["published_date"], defaults["categories"], [], defaults["link"])
            )
            paper_id = cursor.fetchone()[0]
            return Paper(id=paper_id, arxiv_id=arxiv_id,
                         title=defaults["title"], abstract=defaults["abstract"],
                         published_date=defaults["published_date"], categories=["categories"], link=defaults["link"]), True
    
    def update(self, paper):
        """Add authors, keywords, and emeddings to a paper. If the author does not exist, it will be created."""
        with connection.cursor() as cursor:
            # Update the keywords and embedding of the paper
            cursor.execute(
                "UPDATE researchlens_paper SET keywords = %s, embedding = %s WHERE id = %s",
                [json.dumps(paper.keywords), paper.embedding, paper.id]
            )
            
            # Remove all existing authors for the paper
            cursor.execute("DELETE FROM researchlens_paper_authors WHERE paper_id = %s", [paper.id])
            
            # Add the authors to the paper
            for author in paper.authors:
                # Get or create the author
                author_obj, created = AuthorMapper().get_or_create(author.name)
                
                # Add the author to the paper
                cursor.execute(
                    "INSERT INTO researchlens_paper_authors (paper_id, author_id) VALUES (%s, %s)",
                    [paper.id, author_obj.id]
                )
                

class AuthorMapper:
    """This class is responsible for mapping the Author model to the database and providing methods to fetch, create, and update authors from the database."""
    
    def __init__(self):
        self.author_table_name = 'researchlens_author'
    
    def get_by_name(self, name):
        """Fetch an author by its name."""
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, institution FROM researchlens_author WHERE name = %s", [name])
            row = cursor.fetchone()
            if not row:
                return None
            
            return Author(id=row[0], name=row[1], institution=row[2])
        
    def get_or_create(self, name):
        """Create an author by its name if it does not exist. If it exists, return the existing author."""
        
        author = self.get_by_name(name)
        if author:
            return author, False
            
        # If not found, create a new author by inserting it into the database
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO researchlens_author (name) VALUES (%s) RETURNING id, name, institution",
                [name]
            )
            row = cursor.fetchone()
            if not row:
                return None, False
            
        # Return the newly created author
        return Author(id=row[0], name=row[1], institution=row[2]), True


class RelatedPaperMapper:
    """This class is responsible for fetching related papers based on the embedding similarity (L2 norm) from the database."""
    
    def __init__(self):
        self.paper_table_name = 'researchlens_paper'
        self.paper_similarity_table_name = 'researchlens_papersimilarity'
    
    def get(self, paper_id):
        """Fetch 10 related papers for the paper with the given ID based on the embedding similarity (L2 norm)."""
        
        papers = {}
        with connection.cursor() as cursor:
            # Load the embedding of the paper
            cursor.execute("SELECT embedding FROM researchlens_paper WHERE id = %s", [paper_id])
            row = cursor.fetchone()
            if not row:
                return []
            embedding = row[0]
            if not embedding:
                return []
            
            # Query to get the related papers based on the embedding (we sort by cosine similarity)
            query = (
                "SELECT id "
                "FROM researchlens_paper "
                "WHERE id <> %s "
                "ORDER BY embedding <-> %s ASC " # <-> is the operator for L2 distance in pgvector
                "LIMIT 10;" 
            )
            cursor.execute(query, [paper_id, embedding])
            related_ids = [row[0] for row in cursor.fetchall()]
            if not related_ids:
                return []
            
            # Fetch papers and their authors in a single query from the database.
            # This assumes a many-to-many relationship between papers and authors.
            query = ("SELECT p.id, p.arxiv_id, p.title, p.abstract, p.keywords, p.published_date, p.link, p.categories, "
                "a.id, a.name, a.institution "
                "FROM researchlens_paper p "
                "INNER JOIN researchlens_paper_authors pa ON p.id = pa.paper_id "
                "INNER JOIN researchlens_author a ON pa.author_id = a.id "
                f"WHERE p.id IN ({', '.join(['%s'] * len(related_ids))}) "  # Use IN clause
                "ORDER BY p.published_date DESC ")
            cursor.execute(query, related_ids)
            
            
            # Fetch all rows and construct Paper and Author objects
            rows = cursor.fetchall()
            for row in rows:
                paper_id = row[0]
                
                # Create a new Paper object if it doesn't exist
                if paper_id not in papers:
                    paper = Paper(
                        id=row[0],
                        arxiv_id=row[1],
                        title=row[2].replace('\n', ' ').replace('\r', ' ').strip(),
                        abstract=row[3].replace('\n', ' ').replace('\r', ' ').strip(),
                        keywords=json.loads(row[4]) if row[4] else [],
                        published_date=row[5],
                        link=row[6],
                        categories=row[7]
                    )
                    paper.authors = []
                    papers[paper_id] = paper
                
                # Create a new Author object
                author = Author(
                    id=row[8],
                    name=row[9],
                    institution=row[10]
                )
                
                # Avoid duplicate authors
                if author not in papers[paper_id].authors:
                    papers[paper_id].authors.append(author)
                    
        return list(papers.values())


class PaperSimilarityMapper:
    """This class is responsible for mapping the PaperSimilarity model to the database and providing methods to fetch, create, and update paper similarities from the database."""
    
    def __init__(self):
        self.paper_similarity_table_name = 'researchlens_papersimilarity'
    
    def get_by_ids(self, source_paper_id, target_paper_id):
        """Fetch a paper similarity by source and target paper IDs."""
        
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT source_paper_id, target_paper_id, similarity_score "
                "FROM researchlens_papersimilarity "
                "WHERE source_paper_id = %s AND target_paper_id = %s",
                [source_paper_id, target_paper_id]
            )
            row = cursor.fetchone()
            if not row:
                return None
            
            return {
                'source_paper_id': row[0],
                'target_paper_id': row[1],
                'similarity_score': row[2]
            }
    
    def get_or_create(self, source_paper_id, target_paper_id, similarity_score):
        """Get or create a paper similarity by source and target paper IDs. If the similarity does not exist, it will be created with the given parameters."""
        
        similarity = self.get_by_ids(source_paper_id, target_paper_id)
        if similarity:
            return similarity, False
            
        # If not found, create a new paper similarity by inserting it into the database
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO researchlens_papersimilarity (source_paper_id, target_paper_id, similarity_score) "
                "VALUES (%s, %s, %s) RETURNING source_paper_id, target_paper_id, similarity_score",
                [source_paper_id, target_paper_id, similarity_score]
            )
            row = cursor.fetchone()
            if not row:
                return None, False
            
        # Return the newly created paper similarity
        return {
            'source_paper_id': row[0],
            'target_paper_id': row[1],
            'similarity_score': row[2]
        }, True