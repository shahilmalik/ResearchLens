"""
This file contains the Celery tasks for the ResearchLens application. The task includes fetching data from the arXiv API,
processing it to extract relevant information, computing document embeddings and keywords, and storing it in the database.
We use Celery for asynchronous task processing to handle potentially long-running operations without blocking the main application.
"""

from celery import shared_task
import requests
import xml.etree.ElementTree as ET
from sentence_transformers import SentenceTransformer, util
from keybert import KeyBERT
import numpy as np
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

# Import our custom mapper
from .object_relational_mapper import PaperMapper, AuthorMapper, PaperSimilarityMapper

@shared_task
def run_data_preprocess(number_articles, categories):
    # Initialize models for document embeddings and keyword extraction
    model = SentenceTransformer('all-MiniLM-L6-v2')
    kw_model = KeyBERT()
    
    # Map categories to human-readable names
    ARXIV_CATEGORY_MAP = {
        'cs': 'Computer Science',
        'math': 'Mathematics',
        'stat': 'Statistics',
        'econ': 'Economics',
        'physics': 'Physics',
        'q-bio': 'Quantitative Biology',
        'q-fin': 'Quantitative Finance'
    }
    
    # Initialize our mappers to interact with the database via Python objects
    paper_mapper = PaperMapper()
    author_mapper = AuthorMapper()
    paper_similarity_mapper = PaperSimilarityMapper()

    # Iterate through each category and fetch papers
    for cat in categories:
        MAX_RESULTS_PER_PAGE = 100
        category_name = ARXIV_CATEGORY_MAP.get(cat, cat)

        # 1. Fetch and store papers
        for start in range(0, number_articles, min(number_articles, MAX_RESULTS_PER_PAGE)):
            # URL to fetch papers from arXiv and header to identify our application
            url = f"https://export.arxiv.org/api/query?search_query=cat:{cat}.*&start={start}&max_results={min(number_articles, MAX_RESULTS_PER_PAGE)}"
            headers = {
                "User-Agent": "ResearchLens/0.1 (mailto:shahilabdul001@gmail.com,janhagnberger@gmail.com)"
            }

            session = requests.Session()
            retries = Retry(
                total=3,               # Retry up to 3 times
                backoff_factor=1,      # Wait 1s, 2s, then 4s
                status_forcelist=[429, 500, 502, 503, 504],  # Retry on these codes
                raise_on_status=False
            )
            adapter = HTTPAdapter(max_retries=retries)
            session.mount("https://", adapter)

            try:
                response = session.get(url, headers=headers, timeout=30)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch papers from arXiv: {e}")
                return

            # response.content contains the response body, which is XML
            root = ET.fromstring(response.content)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            # 1.1 Extract paper details from XML response and store in the database
            for entry in root.findall('atom:entry', ns):
                arxiv_id = entry.find('atom:id', ns).text.split('/')[-1]
                title = entry.find('atom:title', ns).text.strip()
                abstract = entry.find('atom:summary', ns).text.strip()
                published = entry.find('atom:published', ns).text[:10]

                # Add paper to the paper table
                paper, _ = paper_mapper.get_or_create(
                    arxiv_id=arxiv_id,
                    defaults={'title': title, 'abstract': abstract, 'published_date': published, 'categories': category_name, 'link': entry.find('atom:id', ns).text.strip()}
                )

                # Add the author(s) to the paper and database
                authors = list(set(entry.findall('atom:author', ns))) # Use set to avoid duplicates
                paper_authors = []
                for author in authors:
                    name = author.find('atom:name', ns).text.strip()
                    author_obj, _ = author_mapper.get_or_create(name=name)
                    paper_authors.append(author_obj)
                    
                # Update the paper with the author
                paper.authors = paper_authors
                paper_mapper.update(paper)


            # 2. Extract keywords if not already done
            papers = paper_mapper.get_filtered(keywords=[])
            for paper in papers:
                keywords = kw_model.extract_keywords(paper.abstract, top_n=10)
                paper.keywords = [kw[0] for kw in keywords]
                paper_mapper.update(paper)
            
            # 3. Build similarity graph
            # 3.1 Generate embeddings for each paper if not already done
            papers = paper_mapper.get_filtered(embedding=None)
            for paper in papers:
                embedding = model.encode(paper.abstract).tolist()
                paper.embedding = embedding
                paper_mapper.update(paper)
            
            # 3.2 Calculate pairwise similarities and store in the database. Currently not used when querying for related papers
            papers = paper_mapper.get_excluded(embedding=None)
            for i, paper1 in enumerate(papers):
                for j, paper2 in enumerate(papers[i+1:]):
                    score = float(util.cos_sim(np.array(paper1.embedding), np.array(paper2.embedding)))
                    if score >= 0.75:
                        paper_similarity_mapper.get_or_create(
                            source_paper_id=paper1.id,
                            target_paper_id=paper2.id,
                            similarity_score=score
                        )
            
            # 4. Wait for a while before the next fetch to avoid hitting rate limits
            time.sleep(3)
