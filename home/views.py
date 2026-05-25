from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
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
    featured_projects = Project.objects.filter(featured=True)[:5]

    return render(request, 'home/index.html', {
        'hero': hero,
        'coding_by_category': coding_by_category,
        'it_skills': it_skills,
        'gallery_items': gallery_items,
        'featured_projects': featured_projects,  # ← was missing
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

@require_POST
def gallery_like(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    action = request.POST.get('action')  # 'like' or 'dislike'
    if action == 'like':
        item.likes += 1
        item.save(update_fields=['likes'])
        return JsonResponse({'likes': item.likes})
    elif action == 'unlike':
        item.likes = max(0, item.likes - 1)
        item.save(update_fields=['likes'])
        return JsonResponse({'likes': item.likes})
    elif action == 'dislike':
        item.dislikes += 1
        item.save(update_fields=['dislikes'])
        return JsonResponse({'dislikes': item.dislikes})
    elif action == 'undislike':
        item.dislikes = max(0, item.dislikes - 1)
        item.save(update_fields=['dislikes'])
        return JsonResponse({'dislikes': item.dislikes})
    return JsonResponse({'error': 'invalid action'}, status=400)