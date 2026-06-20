from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Project
from .serializers import ProjectSerializer
from home.models import HeroSection  # add this

def project_list(request):
    return render(request, 'projects/list.html', {
        'projects': Project.objects.all(),
        'categories': Project.distinct_categories(),
        'hero': HeroSection.objects.first(),
    })

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    hero = HeroSection.objects.first()  # add this
    return render(request, 'projects/detail.html', {'project': project, 'hero': hero})

class ProjectListAPI(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectDetailAPI(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class FeaturedProjectsAPI(generics.ListAPIView):
    queryset = Project.objects.filter(featured=True)
    serializer_class = ProjectSerializer