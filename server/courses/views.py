from django.shortcuts import render
from .models import Course

def index(request):
    return render(request, 'courses\index.html', {
        'Courses': Course.objects.all()
    })
