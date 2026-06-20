

# Create your views here.
from django.shortcuts import render
from .models import HeroSection, Skill, GalleryItem
from projects.models import Project
from rest_framework import generics
from .serializers import HeroSectionSerializer, SkillSerializer, GalleryItemSerializer

def home(request):
    hero = HeroSection.objects.first()

    coding_skills = Skill.objects.filter(section='coding')
    it_skills = Skill.objects.filter(section='it_support')

    coding_by_category = {}
    for skill in coding_skills:
        coding_by_category.setdefault(skill.category, []).append(skill)

    gallery_items = GalleryItem.objects.filter(is_active=True)

    return render(request, 'home/index.html', {
        'hero': hero,
        'coding_by_category': coding_by_category,
        'it_skills': it_skills,
        'gallery_items': gallery_items,
        'featured_projects': Project.for_homepage(),
    })

def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)
# api section

class HeroSectionAPI(generics.ListAPIView):
    queryset = HeroSection.objects.all()
    serializer_class = HeroSectionSerializer

class SkillListAPI(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class GalleryListAPI(generics.ListAPIView):
    queryset = GalleryItem.objects.filter(is_active=True)
    serializer_class = GalleryItemSerializer