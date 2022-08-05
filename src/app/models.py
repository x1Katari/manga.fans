import datetime
from django_better_admin_arrayfield.models.fields import ArrayField
from django.db import models
from django.utils import timezone


class Title(models.Model):
    class Meta:
        verbose_name = 'комикс'
        verbose_name_plural = 'Комиксы'
        ordering = ["name"]

    name = models.CharField(verbose_name='Название комикса', max_length=255, unique=True)
    title_src = models.CharField(verbose_name='Ссылка на комикс', max_length=255, unique=True)
    img_src = models.CharField(verbose_name='Ссылка на изображение', max_length=255, blank=True)
    slug = models.SlugField(verbose_name='Слаг', max_length=255, unique=True, blank=True)
    numbers = ArrayField(models.CharField(max_length=255), blank=True, verbose_name='Номера глав')
    count = models.IntegerField(verbose_name='Число глав', default=0, blank=True)
    added_title = models.DateTimeField(verbose_name='Дата добавления', blank=True, null=True,
                                       default=timezone.now)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    class Meta:
        verbose_name = 'главу'
        verbose_name_plural = 'Главы'
        ordering = ["number"]

    title_name = models.ForeignKey(Title, on_delete=models.CASCADE, verbose_name='Название комикса')
    img_src = models.CharField(verbose_name='Ссылка на изображение', max_length=255, blank=True)
    slug = models.SlugField(verbose_name='Слаг', max_length=255, unique=False, default='')
    number = models.IntegerField(verbose_name='Номер главы')
    pages = ArrayField(models.CharField(max_length=255), blank=True, verbose_name='Список спрайтов')
    added_chapter = models.DateTimeField(verbose_name='Дата добавления', blank=True, null=True,
                                         default=datetime.datetime.now)
    available = models.BooleanField(default=True, verbose_name='Доступна')

    def __str__(self):
        return str(self.title_name)
