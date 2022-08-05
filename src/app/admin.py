from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django.contrib import admin
from .models import Title, Chapter


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    model = Title

    list_display = (
        "id",
        "name",
        "title_src",
        "img_src",
        "slug",
        "added_title",
    )

    list_filter = (
        "added_title",
    )

    list_editable = (
        "name",
        "title_src",
        "img_src",
        "slug",
    )
    search_fields = (
        "id",
        "name",
        "slug",
    )

    prepopulated_fields = {
        "slug": [
            "name"
        ]
    }
    date_hierarchy = "added_title"
    save_on_top = True


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin, DynamicArrayMixin):
    model = Chapter

    list_display = (
        "id",
        "title_name",
        "number",
        "available",
        "added_chapter",
    )

    list_filter = (
        "available",
        "added_chapter",
        "title_name",
    )

    list_editable = (
        "title_name",
        "number",
        "available",
    )

    search_fields = (
        "id",
        "title_name__name",
        "number",
    )

    prepopulated_fields = {
        "slug": [
            "title_name"
        ]
    }

    date_hierarchy = "added_chapter"
    save_on_top = True
