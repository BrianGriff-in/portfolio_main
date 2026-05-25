from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Project
from .serializers import ProjectSerializer

def project_list(request):
    projects = Project.objects.all()
    categories = Project.objects.values_list('category', flat=True).distinct()
    context = {
        'projects': projects,
        'categories': categories,
    }
    return render(request, 'projects/list.html', context)

def project_detail(request, pk):                           # ← ADD THIS
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/detail.html', {'project': project})

class ProjectListAPI(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectDetailAPI(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class FeaturedProjectsAPI(generics.ListAPIView):
    queryset = Project.objects.filter(featured=True)
    serializer_class = ProjectSerializer