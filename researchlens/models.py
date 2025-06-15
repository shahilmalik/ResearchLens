from django.db import models
from pgvector.django import VectorField

class Author(models.Model):
    name = models.CharField(max_length=255)
    institution = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Paper(models.Model):
    arxiv_id = models.CharField(max_length=100, unique=True)
    title = models.TextField()
    abstract = models.TextField()
    published_date = models.DateField()
    authors = models.ManyToManyField(Author)
    keywords = models.JSONField(default=list) 
    embedding = VectorField(dimensions=384, null=True)
    link = models.URLField(null=True)
    categories = models.TextField()

    def __str__(self):
        return self.title
    
class PaperSimilarity(models.Model):
    source_paper = models.ForeignKey(Paper, related_name='source_similarities', on_delete=models.CASCADE)
    target_paper = models.ForeignKey(Paper, related_name='target_similarities', on_delete=models.CASCADE)
    similarity_score = models.FloatField()
