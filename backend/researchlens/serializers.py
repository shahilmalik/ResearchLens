from rest_framework import serializers
from .models import Paper

class PaperSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Paper
        fields = [
            'id',
            'title',
            'abstract',
            'keywords',
            'authors',
            'link',
            'categories',
            'published_date'
        ]