
# Create your views here.
import json

from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .gallery_votes import (
    attach_visitor_cookie,
    resolve_visitor_id,
    visitor_votes_for,
)
from .models import HeroSection, Skill, GalleryItem, GalleryVote
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


class GalleryVoteAPI(APIView):
    VALID_VOTES = {'like', 'dislike'}

    def post(self, request):
        visitor_id, needs_visitor_cookie = resolve_visitor_id(request)

        item_id = request.data.get('item_id')
        vote_type = request.data.get('vote_type')

        if vote_type not in self.VALID_VOTES:
            return Response(
                {'error': 'vote_type must be "like" or "dislike".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        gallery_item = get_object_or_404(GalleryItem, pk=item_id, is_active=True)

        existing = GalleryVote.objects.filter(
            gallery_item=gallery_item,
            visitor_id=visitor_id,
        ).first()

        if existing and existing.vote_type == vote_type:
            existing.delete()
            saved_vote = None
        else:
            GalleryVote.objects.update_or_create(
                gallery_item=gallery_item,
                visitor_id=visitor_id,
                defaults={'vote_type': vote_type},
            )
            saved_vote = vote_type

        response = Response({
            'item_id': gallery_item.pk,
            'vote_type': saved_vote,
        })

        if needs_visitor_cookie:
            attach_visitor_cookie(response, visitor_id)

        return response