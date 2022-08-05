from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.catalog_page, name='catalog'),
    path('<slug:slug>', views.ChaptersDetailView.as_view(), name='chapters'),
    path('<slug:slug>/<int:number>', views.ChapterDetailView.as_view(), name='chapter'),

]