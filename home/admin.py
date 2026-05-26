from django.contrib import admin
from django.utils.html import format_html
from .models import HeroSection, Skill, GalleryItem


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'availability', 'email', 'profile_preview')
    readonly_fields = ('profile_preview',)

    fieldsets = (
    ('Identity', {
        'fields': ('name', 'profile_image', 'profile_preview', 'bio', 'tagline', 'favicon')  # add favicon here
    }),
    ('Personal Info', {
        'fields': ('location', 'availability', 'languages', 'interests')
    }),
    ('Contact & Links', {
        'fields': ('email', 'github_url', 'linkedin_url', 'resume')
    }),
    ("Let's Work Together", {
        'fields': ('contact_blurb',)
    }),
    )

    def profile_preview(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:50%"/>',
                obj.profile_image.url
            )
        return '—'
    profile_preview.short_description = 'Preview'


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'icon_class', 'order')
    list_filter = ('category',)
    search_fields = ('name',)
    list_editable = ('order', 'proficiency')


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'order', 'is_active', 'image_preview')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:70px;border-radius:8px;object-fit:cover;"/>',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'Preview'