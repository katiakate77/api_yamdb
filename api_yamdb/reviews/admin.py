from django.contrib import admin
from .models import Category, Genre, Title, GenreTitle


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description', 'category')
    search_fields = ('text',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre', 'title')
    search_fields = ('genre', 'title')
    list_filter = ('genre', 'title')
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
