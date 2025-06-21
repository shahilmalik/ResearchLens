class Author():
    
    def __init__(self, id="", name="", institution=None):
        self.id = id
        self.name = name
        self.institution = institution

    def __str__(self):
        return str(self.name)
    
    

class Paper():
    
    def __init__(self, id="", arxiv_id="", title="", abstract="", published_date=None, authors=None, keywords=None, embedding=None, link=None, categories=""):
        self.id = id
        self.arxiv_id = arxiv_id
        self.title = title
        self.abstract = abstract
        self.published_date = published_date
        self.authors = authors if authors is not None else []
        self.keywords = keywords if keywords is not None else []
        self.embedding = embedding
        self.link = link
        self.categories = categories

    def __str__(self):
        return str(self.title)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "abstract": self.abstract,
            "keywords": self.keywords,
            "authors": [author.name for author in self.authors],
            "link": self.link,
            "categories": self.categories,
            "published_date": self.published_date.isoformat() if self.published_date else None,
        }

class PaperSimilarity():
    def __init__(self, source_paper=None, target_paper=None, similarity_score=0.0):
        self.source_paper = source_paper
        self.target_paper = target_paper
        self.similarity_score = similarity_score

    def __str__(self):
        return f"{self.source_paper.title} <-> {self.target_paper.title} : {self.similarity_score}"
    
    def to_dict(self):
        return {
            "source_paper": self.source_paper.to_dict(),
            "target_paper": self.target_paper.to_dict(),
            "similarity_score": self.similarity_score,
        }