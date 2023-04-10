from django.contrib import admin

from .models import Category, Genre, Title, GenreTitle


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description', 'category')
    search_fields = ('text',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre', 'title')
    search_fields = ('genre', 'title')
    list_filter = ('genre', 'title')
    empty_value_display = '-пусто-'
