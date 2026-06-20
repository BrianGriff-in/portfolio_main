from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('<int:pk>/', views.project_detail, name='detail'),

    # API routes
    path('api/projects/', views.ProjectListAPI.as_view(), name='api-list'),
    path('api/projects/<int:pk>/', views.ProjectDetailAPI.as_view(), name='api-detail'),
    path('api/projects/featured/', views.FeaturedProjectsAPI.as_view(), name='api-featured'),

]