from django.contrib import admin
from .models import Paper, Author, PaperSimilarity

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'arxiv_id', 'published_date')
    search_fields = ('title', 'abstract', 'keywords')
    list_filter = ('published_date',)
    filter_horizontal = ('authors',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(PaperSimilarity)
class PaperSimilarityAdmin(admin.ModelAdmin):
    list_display = ('source_paper', 'target_paper', 'similarity_score')
    search_fields = ('source_paper__title', 'target_paper__title')
