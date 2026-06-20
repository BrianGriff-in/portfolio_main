from datetime import date

from django.test import TestCase

from projects.models import Project


class ProjectQueryTests(TestCase):
    def setUp(self):
        self.base = dict(
            description='Test project',
            tech_stack='Django',
            thumbnail='test/image',
            created_at=date(2024, 1, 1),
        )

    def test_distinct_categories_deduplicates_with_ordering(self):
        Project.objects.create(title='A', category='Web', **self.base)
        Project.objects.create(title='B', category='Web', **self.base)
        Project.objects.create(title='C', category='API', **self.base)

        categories = Project.distinct_categories()

        self.assertEqual(categories, [
            {'value': 'API', 'label': 'API'},
            {'value': 'Web', 'label': 'Web'},
        ])

    def test_distinct_categories_uses_display_labels(self):
        Project.objects.create(title='ML Project', category='ML', **self.base)

        categories = Project.distinct_categories()

        self.assertEqual(categories, [{'value': 'ML', 'label': 'Machine Learning'}])

    def test_for_homepage_prefers_featured_projects(self):
        featured = Project.objects.create(
            title='Featured', category='Web', featured=True, **self.base
        )
        Project.objects.create(title='Regular', category='API', **self.base)

        homepage_projects = list(Project.for_homepage())

        self.assertEqual(homepage_projects, [featured])

    def test_for_homepage_falls_back_to_latest_when_none_featured(self):
        older = Project.objects.create(
            title='Older', category='Web', **{**self.base, 'created_at': date(2023, 1, 1)}
        )
        newer = Project.objects.create(
            title='Newer', category='API', **{**self.base, 'created_at': date(2024, 6, 1)}
        )

        homepage_projects = list(Project.for_homepage(limit=2))

        self.assertEqual(homepage_projects, [newer, older])