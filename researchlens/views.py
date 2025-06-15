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
    run_data_preprocess.delay()  
    return Response({"status": "Data fetching and preprocessing started"})

class PaperListView(generics.ListAPIView):
    queryset = Paper.objects.all().order_by('-published_date')
    serializer_class = PaperSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'abstract', 'authors__name']
    pagination_class = CustomPagination 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PaperFilter


class RelatedPapersView(APIView):
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