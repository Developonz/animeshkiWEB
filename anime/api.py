from rest_framework import viewsets, status
from .models import Anime, Genre, Studio, Director, Status, Country
from .serializers import AnimeSerializer, GenreSerializer, StudioSerializer, DirectorSerializer, StatusSerializer, CountrySerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Max, Min, F


# Вьюсет для модели Anime
class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Пожалуйста, авторизуйтесь для просмотра списка аниме")
            
        qs = super().get_queryset()
        user_filter = self.request.query_params.get('user', None)
        
        if self.request.user.is_superuser:
            if user_filter and user_filter != 'all':
                return qs.filter(user__username=user_filter)
            return qs
        return qs.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def users(self, request):
        if request.user.is_superuser:
            users = User.objects.filter(anime__isnull=False).distinct()
            return Response([user.username for user in users])
        return Response([])

    @action(detail=False, methods=['GET'], url_path="stats")
    def stats(self, request):
        queryset = self.get_queryset() 
        stats = {
            'Всего аниме:': queryset.count(),
            'Распределение по статусу:': dict(
                queryset.values('status__name')
                .annotate(count=Count('id'))
                .values_list('status__name', 'count')
            ),
            'Максимум аниме в году:': dict(
                queryset.filter(date__isnull=False)  # Исключаем записи без дат
                .annotate(year=F('date__year'))  # Добавляем год как отдельное поле
                .values('year')  # Группируем по году
                .annotate(count=Count('id'))  # Считаем количество записей для каждого года
                .order_by('-count')[:1]
                .values_list('date__year', 'count')
            )
        }
        return Response(stats)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    @action(detail=False, methods=['GET'], url_path="stats")
    def stats(self, request):
        stats = {
            'Всего жанров:': Genre.objects.count(),
            'Наиболее популярный жанр:': Genre.objects.annotate(
                usage_count=Count('anime')
            ).order_by('-usage_count').first().name,
            'Наименее популярный жанр:': Genre.objects.annotate(
                usage_count=Count('anime')
            ).order_by('usage_count').first().name
        }
        return Response(stats)

class StudioViewSet(viewsets.ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer

    @action(detail=False, methods=['GET'], url_path="stats")
    def stats(self, request):
        stats = {
            'Всего студий:': Studio.objects.count(),
            'Наиболее продуктивная студия:': Studio.objects.annotate(
                works_count=Count('anime')
            ).order_by('-works_count').first().name
        }
        return Response(stats)

class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    @action(detail=False, methods=['GET'], url_path="stats")
    def stats(self, request):
        stats = {
            'Всего режиссёров:': Director.objects.count(),
            'Самый опытный режиссер:': Director.objects.annotate(
                years_active=Max('anime__date') - Min('anime__date')
            ).order_by('-years_active').first().name
        }
        return Response(stats)

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class UserProfileViewSet(GenericViewSet):
    @action(url_path="info", detail=False, methods=['get'])
    def info(self, request, *args, **kwargs):
        user = request.user
        data = {"is_authenticated": user.is_authenticated}
        if user.is_authenticated:
            data.update({"is_superuser": user.is_superuser, "name": user.username})
        return Response(data)
    
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    @action(detail=False, methods=['GET'], url_path="stats")
    def stats(self, request):
        stats = {
            'Всего стран:': Country.objects.count(),
            'Больше всего студий в:': Country.objects.annotate(
                studios_count=Count('studio')
            ).order_by('-studios_count').first().name
        }
        return Response(stats)
