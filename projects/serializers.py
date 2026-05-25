from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    tech_list = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description',
            'tech_stack', 'tech_list',
            'thumbnail', 'live_url', 'github_url',
            'featured', 'created_at', 'category'
        ]

    def get_thumbnail(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.url
        return None

    def get_tech_list(self, obj):
        return obj.tech_list()