import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from rest_framework import generics

from .gallery_votes import (
    apply_gallery_vote,
    attach_visitor_cookie,
    resolve_visitor_id,
    visitor_votes_for,
)
from .models import HeroSection, Skill, GalleryItem
from projects.models import Project
from .serializers import HeroSectionSerializer, SkillSerializer, GalleryItemSerializer


@ensure_csrf_cookie
def home(request):
    hero = HeroSection.objects.first()

    coding_skills = Skill.objects.filter(section='coding')
    it_skills = Skill.objects.filter(section='it_support')

    coding_by_category = {}
    for skill in coding_skills:
        coding_by_category.setdefault(skill.category, []).append(skill)

    gallery_items = GalleryItem.objects.filter(is_active=True)
    visitor_id, needs_visitor_cookie = resolve_visitor_id(request)

    response = render(request, 'home/index.html', {
        'hero': hero,
        'coding_by_category': coding_by_category,
        'it_skills': it_skills,
        'gallery_items': gallery_items,
        'featured_projects': Project.for_homepage(),
        'gallery_votes_json': json.dumps(visitor_votes_for(visitor_id)),
    })

    if needs_visitor_cookie:
        attach_visitor_cookie(response, visitor_id)

    return response


def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)


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
    visitor_id, needs_visitor_cookie = resolve_visitor_id(request)
    item = get_object_or_404(GalleryItem, pk=pk, is_active=True)
    action = request.POST.get('action')

    if action not in ('like', 'dislike'):
        return JsonResponse({'error': 'action must be "like" or "dislike".'}, status=400)

    saved_vote, item = apply_gallery_vote(item, visitor_id, action)
    response = JsonResponse({
        'vote_type': saved_vote,
        'likes': item.likes,
        'dislikes': item.dislikes,
    })

    if needs_visitor_cookie:
        attach_visitor_cookie(response, visitor_id)

    return response