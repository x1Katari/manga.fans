from django.shortcuts import render, HttpResponse
from .models import Chapter

def index(request):
    things = Chapter.objects.first()
    return HttpResponse(f'<h1>{things.pages[0]}</h1>'
                        f'<h2>{things.pages[1]}</h2>')