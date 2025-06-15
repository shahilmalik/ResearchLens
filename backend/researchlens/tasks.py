from celery import shared_task
import requests
import xml.etree.ElementTree as ET
from .models import Paper, Author, PaperSimilarity
from sentence_transformers import SentenceTransformer, util
from keybert import KeyBERT
import numpy as np
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

@shared_task
def run_data_preprocess():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    kw_model = KeyBERT()
    # 1. Fetch and store papers
    CATEGORIES = ['cs', 'math', 'stat', 'econ', 'physics', 'q-bio', 'q-fin']
    ARXIV_CATEGORY_MAP = {
    'cs': 'Computer Science',
    'math': 'Mathematics',
    'stat': 'Statistics',
    'econ': 'Economics',
    'physics': 'Physics',
    'q-bio': 'Quantitative Biology',
    'q-fin': 'Quantitative Finance'
}


    for cat in CATEGORIES:
        MAX_RESULTS_PER_PAGE = 100
        TOTAL_RESULTS = 1000  # or more, if you want like 5000 per category
        category_name = ARXIV_CATEGORY_MAP.get(cat, cat)

        for start in range(0, TOTAL_RESULTS, MAX_RESULTS_PER_PAGE):
            url = f"https://export.arxiv.org/api/query?search_query=cat:{cat}&start={start}&max_results={MAX_RESULTS_PER_PAGE}"

            headers = {
                "User-Agent": "ResearchLens/0.1 (mailto:shahilabdul001@gmail.com)"
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

            root = ET.fromstring(response.content)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            for entry in root.findall('atom:entry', ns):
                arxiv_id = entry.find('atom:id', ns).text.split('/')[-1]
                title = entry.find('atom:title', ns).text.strip()
                abstract = entry.find('atom:summary', ns).text.strip()
                published = entry.find('atom:published', ns).text[:10]

                paper, created = Paper.objects.get_or_create(
                    arxiv_id=arxiv_id,
                    defaults={'title': title, 'abstract': abstract, 'published_date': published, 'categories' : category_name, 'link': entry.find('atom:id', ns).text.strip()}
                )

                authors = entry.findall('atom:author', ns)
                for author in authors:
                    name = author.find('atom:name', ns).text.strip()
                    author_obj, _ = Author.objects.get_or_create(name=name)
                    paper.authors.add(author_obj)

            # 2. Extract keywords and embeddings
            papers = Paper.objects.all()
            for paper in papers:
                keywords = kw_model.extract_keywords(paper.abstract, top_n=10)
                paper.keywords = [kw[0] for kw in keywords]
                embedding = model.encode(paper.abstract).tolist()
                paper.embedding = embedding
                paper.save()

            # 3. Build similarity graph
            papers = list(Paper.objects.exclude(embedding=None))
            for i, paper1 in enumerate(papers):
                for j, paper2 in enumerate(papers):
                    if i >= j:
                        continue
                    score = float(util.cos_sim(np.array(paper1.embedding), np.array(paper2.embedding)))
                    if score >= 0.75:
                        PaperSimilarity.objects.get_or_create(
                            source_paper=paper1,
                            target_paper=paper2,
                            similarity_score=score
                        )
            time.sleep(3)
