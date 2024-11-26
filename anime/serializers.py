from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from .models import Anime, Status, Studio, Director, Genre, Country

class AnimeSerializer(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), allow_null=False)
    date = serializers.DateField(allow_null=True, required=False)
    studio = serializers.PrimaryKeyRelatedField(queryset=Studio.objects.all(), allow_null=True, required=False)
    director = serializers.PrimaryKeyRelatedField(queryset=Director.objects.all(), allow_null=True, required=False)
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True, required=True)
    picture_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Anime
        fields = '__all__'

    def get_picture_url(self, obj):
        request = self.context.get('request')
        if obj.picture and hasattr(obj.picture, 'url'):
            return request.build_absolute_uri(obj.picture.url)
        return None

    def validate(self, data):
        status = data.get('status')
        if status and status.name.lower() != 'анонс':
            if not data.get('studio') and not data.get('director'):
                raise serializers.ValidationError({
                    'studio': 'Для не анонсированного аниме студия и режиссёр обязательны'
                })
            if not data.get('studio'):
                raise serializers.ValidationError({
                    'studio': 'Для не анонсированного аниме студия обязательна'
                })
            if not data.get('director'):
                raise serializers.ValidationError({
                    'director': 'Для не анонсированного аниме директор обязателен'
                })
        genres = data.get('genres')
        if not genres:
            raise serializers.ValidationError({
                'genres': 'Поле "Жанры" обязательно для заполнения.'
            })
        return data

    def create(self, validated_data):
        genres = validated_data.pop('genres', [])
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        anime = Anime.objects.create(**validated_data)
        anime.genres.set(genres)
        return anime

    def update(self, instance, validated_data):
        genres = validated_data.pop('genres', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if genres is not None:
            instance.genres.set(genres)
        return instance
    



class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = '__all__'

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
