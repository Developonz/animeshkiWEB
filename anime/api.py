from rest_framework import viewsets, status
from .models import Anime, Genre, Studio, Director, Status, Country
from .serializers import AnimeSerializer, GenreSerializer, StudioSerializer, DirectorSerializer, StatusSerializer, CountrySerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from django.contrib.auth.models import User


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


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class StudioViewSet(viewsets.ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer

class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

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
