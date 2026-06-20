import uuid

VISITOR_COOKIE = 'gallery_visitor_id'
VISITOR_COOKIE_MAX_AGE = 60 * 60 * 24 * 365


def resolve_visitor_id(request):
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


def apply_gallery_vote(item, visitor_id, vote_type):
    """Set like/dislike for a visitor, keeping counts and votes mutually exclusive."""
    from .models import GalleryVote

    existing = GalleryVote.objects.filter(
        gallery_item=item,
        visitor_id=visitor_id,
    ).first()

    if vote_type not in ('like', 'dislike'):
        raise ValueError('vote_type must be "like" or "dislike".')

    if existing and existing.vote_type == vote_type:
        if existing.vote_type == 'like':
            item.likes = max(0, item.likes - 1)
        else:
            item.dislikes = max(0, item.dislikes - 1)
        existing.delete()
        item.save(update_fields=['likes', 'dislikes'])
        return None, item

    if existing:
        if existing.vote_type == 'like':
            item.likes = max(0, item.likes - 1)
            item.dislikes += 1
        else:
            item.dislikes = max(0, item.dislikes - 1)
            item.likes += 1
        existing.vote_type = vote_type
        existing.save(update_fields=['vote_type', 'updated_at'])
        item.save(update_fields=['likes', 'dislikes'])
        return vote_type, item

    GalleryVote.objects.create(
        gallery_item=item,
        visitor_id=visitor_id,
        vote_type=vote_type,
    )
    if vote_type == 'like':
        item.likes += 1
    else:
        item.dislikes += 1
    item.save(update_fields=['likes', 'dislikes'])
    return vote_type, item