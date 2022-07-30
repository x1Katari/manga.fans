from django.db import models


class Title(models.Model):
    class Meta:
        verbose_name = 'комикс'
        verbose_name_plural = 'Комиксы'
        ordering = ["name"]

    name = models.CharField(verbose_name='Название комикса', max_length=255, unique=True)
    title_src = models.CharField(verbose_name='Ссылка на комикс', max_length=255, unique=True)
    img_src = models.CharField(verbose_name='Ссылка на изображение', max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    added_title = models.DateTimeField(verbose_name='Дата добавления', blank=True, null=True)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    class Meta:
        verbose_name = 'главу'
        verbose_name_plural = 'Главы'
        ordering = ["number"]

    title_name = models.ForeignKey(Title, on_delete=models.PROTECT, verbose_name='Название комикса')
    number = models.IntegerField(verbose_name='Номер главы')
    pages = models.TextField(verbose_name='Список спрайтов')
    added_chapter = models.DateTimeField(verbose_name='Дата добавления', blank=True, null=True)
    available = models.BooleanField(default=True, verbose_name='Доступна')

    def __str__(self):
        return str(self.title_name) + str(self.number)