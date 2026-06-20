import json

from django.test import TestCase, Client
from django.urls import reverse

from home.gallery_votes import VISITOR_COOKIE
from home.models import GalleryItem, GalleryVote


class GalleryVoteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.item = GalleryItem.objects.create(
            image='gallery/test',
            title='Test Photo',
            subtitle='Subtitle',
        )
        self.visitor_id = 'visitor-test-123'

    def test_vote_is_mutually_exclusive(self):
        GalleryVote.objects.create(
            gallery_item=self.item,
            visitor_id=self.visitor_id,
            vote_type='like',
        )

        self.client.cookies[VISITOR_COOKIE] = self.visitor_id
        response = self.client.post(
            reverse('home:api-gallery-vote'),
            data=json.dumps({'item_id': self.item.pk, 'vote_type': 'dislike'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['vote_type'], 'dislike')
        self.assertEqual(GalleryVote.objects.count(), 1)
        self.assertEqual(
            GalleryVote.objects.get(gallery_item=self.item).vote_type,
            'dislike',
        )

    def test_toggling_same_vote_removes_it(self):
        GalleryVote.objects.create(
            gallery_item=self.item,
            visitor_id=self.visitor_id,
            vote_type='like',
        )

        self.client.cookies[VISITOR_COOKIE] = self.visitor_id
        response = self.client.post(
            reverse('home:api-gallery-vote'),
            data=json.dumps({'item_id': self.item.pk, 'vote_type': 'like'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()['vote_type'])
        self.assertEqual(GalleryVote.objects.count(), 0)

    def test_visitor_votes_for_restores_saved_vote(self):
        from home.gallery_votes import visitor_votes_for

        GalleryVote.objects.create(
            gallery_item=self.item,
            visitor_id=self.visitor_id,
            vote_type='like',
        )

        votes = visitor_votes_for(self.visitor_id)

        self.assertEqual(votes[self.item.pk], 'like')