from django.db import models
from cloudinary.models import CloudinaryField


class HeroSection(models.Model):
    AVAILABILITY_CHOICES = [
        ('open', 'Open to Opportunities'),
        ('freelance', 'Freelance Only'),
        ('internship', 'Internship Only'),
        ('unavailable', 'Not Available'),
    ]

    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200)
    bio = models.TextField()
    profile_image = CloudinaryField('image')
    resume = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    email = models.EmailField()
    location = models.CharField(max_length=100, default='Phnom Penh, Cambodia')
    availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='open'
    )
    languages = models.CharField(
        max_length=200,
        default='Khmer (Native), English (Professional)',
    )
    interests = models.CharField(
        max_length=200,
        default='Fintech, Web Development, Open Source',
    )
    contact_blurb = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def resume_download_url(self):
        return self.resume or None

    class Meta:
        verbose_name = 'Hero Section'


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Database', 'Database'),
        ('Tools', 'Tools'),
        ('Other', 'Other'),
    ]
    SECTION_CHOICES = [
        ('coding', 'Coding'),
        ('it_support', 'IT Support'),
    ]

    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100)
    proficiency = models.IntegerField(default=80)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default='coding')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name']


class GalleryItem(models.Model):
    image = CloudinaryField('image')
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)       
    dislikes = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = 'Gallery Item'
        verbose_name_plural = 'Gallery Items'