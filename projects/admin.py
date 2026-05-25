from django.contrib import admin
from django.utils.html import format_html
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured', 'created_at', 'thumbnail_preview')
    list_filter = ('category', 'featured')
    search_fields = ('title', 'description', 'tech_stack')
    list_editable = ('featured',)
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="height:60px;border-radius:6px"/>', obj.thumbnail.url)
        return '—'
    thumbnail_preview.short_description = 'Thumbnail'