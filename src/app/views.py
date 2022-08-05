from django.shortcuts import render, HttpResponse
from django.views import generic

from .models import Chapter, Title


def catalog_page(request):
    titles = Title.objects.filter(count__gt=0).order_by('-count')
    return render(request, 'app/catalog.html', {'titles': titles})


class ChaptersDetailView(generic.DetailView):
    model = Title
    template_name = 'app/chapters.html'
    context_object_name = 'title'

class ChapterDetailView(generic.DetailView):
    model = Chapter
    template_name = 'app/chapter.html'
    context_object_name = 'chapter'

    def get_queryset(self):
        return Chapter.objects.filter(slug=self.kwargs['slug']).filter(number=self.kwargs['number'])
