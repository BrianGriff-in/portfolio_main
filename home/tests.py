import json

from django.test import TestCase, Client
from django.urls import reverse

from home.gallery_votes import VISITOR_COOKIE, apply_gallery_vote, visitor_votes_for
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

    def test_apply_gallery_vote_is_mutually_exclusive(self):
        GalleryVote.objects.create(
            gallery_item=self.item,
            visitor_id=self.visitor_id,
            vote_type='like',
        )
        self.item.likes = 1
        self.item.save(update_fields=['likes'])

        vote_type, item = apply_gallery_vote(self.item, self.visitor_id, 'dislike')

        self.assertEqual(vote_type, 'dislike')
        self.assertEqual(item.likes, 0)
        self.assertEqual(item.dislikes, 1)
        self.assertEqual(GalleryVote.objects.get(gallery_item=self.item).vote_type, 'dislike')

    def test_apply_gallery_vote_toggles_off_same_choice(self):
        GalleryVote.objects.create(
            gallery_item=self.item,
            visitor_id=self.visitor_id,
            vote_type='like',
        )
        self.item.likes = 1
        self.item.save(update_fields=['likes'])

        vote_type, item = apply_gallery_vote(self.item, self.visitor_id, 'like')

        self.assertIsNone(vote_type)
        self.assertEqual(item.likes, 0)
        self.assertEqual(GalleryVote.objects.count(), 0)

    def test_gallery_like_endpoint_persists_vote(self):
        self.client.cookies[VISITOR_COOKIE] = self.visitor_id
        response = self.client.post(
            reverse('home:gallery-like', kwargs={'pk': self.item.pk}),
            data={'action': 'like'},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['vote_type'], 'like')
        self.assertEqual(payload['likes'], 1)
        self.assertEqual(visitor_votes_for(self.visitor_id)[self.item.pk], 'like')

    def test_gallery_like_endpoint_switches_vote(self):
        GalleryVote.objects.create(
            gallery_item=self.item,
            visitor_id=self.visitor_id,
            vote_type='like',
        )
        self.item.likes = 1
        self.item.save(update_fields=['likes'])

        self.client.cookies[VISITOR_COOKIE] = self.visitor_id
        response = self.client.post(
            reverse('home:gallery-like', kwargs={'pk': self.item.pk}),
            data={'action': 'dislike'},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['vote_type'], 'dislike')
        self.assertEqual(payload['likes'], 0)
        self.assertEqual(payload['dislikes'], 1)