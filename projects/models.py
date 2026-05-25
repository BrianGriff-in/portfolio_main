from django.db import models
from cloudinary.models import CloudinaryField

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('Web', 'Web'),
        ('Mobile', 'Mobile'),
        ('API', 'API'),
        ('ML', 'Machine Learning'),
        ('Other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=300, help_text='Comma-separated, e.g. Django, React, PostgreSQL')
    thumbnail = CloudinaryField('image')
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',')]

    class Meta:
        ordering = ['-created_at']