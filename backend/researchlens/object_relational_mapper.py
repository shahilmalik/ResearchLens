from django.db import connection
from .custom_models import Paper, Author
import json


class PaperMapper:
    def __init__(self):
        self.paper_table_name = 'researchlens_paper'
        self.author_table_name = 'researchlens_author'
        self.paper_authors_table_name = 'researchlens_paper_authors'
    
    def get(self, page=1, page_size=10, search="", start_date=None, end_date=None, categories=None):
        """Fetch a page with papers and their authors from the database ordered by publication date and filtered
        by the provided filtering elements."""
        
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


class RelatedPaperMapper:
    def __init__(self):
        self.paper_table_name = 'researchlens_paper'
        self.paper_similarity_table_name = 'researchlens_papersimilarity'
    
    def get(self, paper_id):
        """Fetch 10 related papers"""
        
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