"""
This file contains the views for the ResearchLens application, including API endpoints for fetching and processing research papers.
The file contains only little code because the actual logic is handled by Django.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import run_data_preprocess
from django.db.models import F
from pgvector.django import L2Distance
from rest_framework import generics, filters
from .models import Paper
from .serializers import PaperSerializer
from .pagination import CustomPagination
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .filters import PaperFilter
from django_filters.rest_framework import DjangoFilterBackend


@api_view(['POST'])
def start_fetch(request):
    """Starts the data fetching and preprocessing task."""
    
    number_articles = int(request.GET.get("number_articles", 10))
    categories = request.GET.get("categories", ",".join(['cs', 'math'])).split(',')
    print(f"Starting data fetch with {number_articles} articles from categories: {categories}")
    run_data_preprocess.delay(number_articles, categories)
    
    return Response({"status": "Data fetching and preprocessing started"})


class PaperListView(generics.ListAPIView):
    """Fetches a paginated list of papers based on search criteria."""
    
    queryset = Paper.objects.all().order_by('-published_date')
    serializer_class = PaperSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'abstract', 'authors__name']
    pagination_class = CustomPagination 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PaperFilter


class RelatedPapersView(APIView):
    """Fetches related papers based on a given paper ID."""
     
    def get(self, request, paper_id):
        paper = get_object_or_404(Paper, id=paper_id)
        embedding = paper.embedding

        related_papers = (
            Paper.objects
            .exclude(id=paper_id) 
            .annotate(distance=L2Distance("embedding", embedding))
            .order_by("distance")[:10]
        )

        return Response(PaperSerializer(related_papers, many=True).data)