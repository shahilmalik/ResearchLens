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

# custom object relational mappers (ORMs) to explicitly handle database interactions
from .object_relational_mapper import PaperMapper, RelatedPaperMapper

@api_view(['POST'])
def start_fetch(request):
    number_articles = int(request.GET.get("number_articles", 10))
    categories = request.GET.get("categories", ",".join(['cs', 'math'])).split(',')
    print(f"Starting data fetch with {number_articles} articles from categories: {categories}")
    run_data_preprocess.delay(number_articles, categories)
    return Response({"status": "Data fetching and preprocessing started"})


class PaperListView(APIView):
    def get(self, request):
        search = request.GET.get('search', '')
        start = request.GET.get('start_date', '')
        end = request.GET.get('end_date', '')
        cat = request.GET.get('categories', '')
        page = int(request.GET.get('page', 1))
        PAGE_SIZE = 10  # Default page size

        # Use the custom ORM to fetch papers
        paper_mapper = PaperMapper()
        total_count, papers = paper_mapper.get(page=page, page_size=PAGE_SIZE, search=search, start_date=start, end_date=end, categories=cat)

        # Serialize the papers into JSON format
        serialized_papers = [paper.to_dict() for paper in papers]
        
        # Return the paginated response
        return Response({
            'current_page': page,
            'total_pages': total_count//PAGE_SIZE + (1 if total_count % PAGE_SIZE > 0 else 0),
            'total_items': total_count,
            'results': serialized_papers
        })


class RelatedPapersView(APIView):
    def get(self, request, paper_id):
        mapper = RelatedPaperMapper()
        related_papers = mapper.get(paper_id)
        
        serialized_papers = [paper.to_dict() for paper in related_papers]

        return Response(serialized_papers)