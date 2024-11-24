from rest_framework import viewsets
from .models import Anime, Genre, Studio, Director, Status, Country
from .serializers import AnimeSerializer, GenreSerializer, StudioSerializer, DirectorSerializer, StatusSerializer, CountrySerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet


# Вьюсет для модели Anime
class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
  

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
    def get_url(self, request, *args, **kwargs):
        user = request.user
        data = {"is_authenticated": user.is_authenticated}
        if user.is_authenticated:
            data.update({"is_superuser": user.is_superuser, "name" : user.username})
        return Response(data)
    
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
