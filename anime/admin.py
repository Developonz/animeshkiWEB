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
    def get_list_display(self, request):
        # Проверка на статус "анонс"
        if request.GET.get('status__exact') == 'Анонс':
            return ['title_name', 'status', 'studio', 'director']
        return ['title_name', 'status', 'studio', 'director', 'date', 'genres'] 
