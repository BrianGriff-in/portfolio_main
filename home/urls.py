from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='index'),

    # API routes
    path('api/hero/', views.HeroSectionAPI.as_view(), name='api-hero'),
    path('api/skills/', views.SkillListAPI.as_view(), name='api-skills'),
    path('api/gallery/', views.GalleryListAPI.as_view(), name='api-gallery'),
    path('gallery/<int:pk>/like/', views.gallery_like, name='gallery-like'),
]