import uuid

from django.http import HttpResponse

VISITOR_COOKIE = 'gallery_visitor_id'
VISITOR_COOKIE_MAX_AGE = 60 * 60 * 24 * 365


def resolve_visitor_id(request):
    """Return the visitor id from the cookie, creating one if missing."""
    visitor_id = request.COOKIES.get(VISITOR_COOKIE)
    if visitor_id:
        return visitor_id, False
    return str(uuid.uuid4()), True


def attach_visitor_cookie(response, visitor_id):
    response.set_cookie(
        VISITOR_COOKIE,
        visitor_id,
        max_age=VISITOR_COOKIE_MAX_AGE,
        httponly=True,
        samesite='Lax',
    )
    return response


def visitor_votes_for(visitor_id):
    if not visitor_id:
        return {}
    from .models import GalleryVote

    return dict(
        GalleryVote.objects.filter(visitor_id=visitor_id).values_list(
            'gallery_item_id', 'vote_type'
        )
    )