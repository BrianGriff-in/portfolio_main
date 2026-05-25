from rest_framework import serializers
from .models import HeroSection, Skill, GalleryItem


class HeroSectionSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()

    class Meta:
        model = HeroSection
        fields = [
            'id', 'name', 'tagline', 'bio',
            'profile_image', 'resume',
            'github_url', 'linkedin_url', 'email',
            'location', 'availability',
            'languages', 'interests', 'contact_blurb',
        ]

    def get_profile_image(self, obj):
        if obj.profile_image:
            return obj.profile_image.url  # ← full Cloudinary URL
        return None

    def get_resume(self, obj):
        if obj.resume:
            url = obj.resume.url.replace('/upload/', '/upload/fl_attachment/')
            url = url.replace('http://', 'https://')  # ← force https
            return url
        return None


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'icon_class',
            'proficiency', 'category', 'section', 'order'
        ]


class GalleryItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = GalleryItem
        fields = [
            'id', 'title', 'subtitle',
            'image', 'link', 'order', 'is_active'
        ]

    def get_image(self, obj):
        if obj.image:
            return obj.image.url  # ← full Cloudinary URL
        return None