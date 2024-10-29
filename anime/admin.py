from django.contrib import admin
from .models import Country, Studio, Director, Genre, Status, Anime

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country']

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    filter_horizontal = ('genres',)

    def get_list_display(self, request):
        if request.GET.get('status__exact') == 'Анонс':
            return ['title_name', 'status', 'studio', 'director']
        return ['title_name', 'status', 'studio', 'director', 'date', 'display_genres']

    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    display_genres.short_description = 'Жанры' 
