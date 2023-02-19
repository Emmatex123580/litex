from django.shortcuts import render
from .models import Project
# Create your views here.
def index(request):
    project = Project.objects.all()
    context = {
        'project': project
    }
    return render(request, 'index.html', context)