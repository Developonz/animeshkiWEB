from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from .models import Anime, Status, Studio, Director, Genre, Country

class AnimeSerializer(serializers.ModelSerializer):
    picture_url = serializers.SerializerMethodField(read_only=True)

    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), allow_null=False)
    director = serializers.PrimaryKeyRelatedField(queryset=Director.objects.all(), allow_null=True, required=False)
    studio = serializers.PrimaryKeyRelatedField(queryset=Studio.objects.all(), allow_null=True, required=False)
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True, required=True)
    date = serializers.DateField(allow_null=True, required=False)

    class Meta:
        model = Anime
        fields = '__all__'

    def get_picture_url(self, obj):
        request = self.context.get('request')
        if obj.picture and hasattr(obj.picture, 'url'):
            return request.build_absolute_uri(obj.picture.url)
        return None

    def validate_genres(self, value):
        if not value:
            raise serializers.ValidationError('Поле "Жанры" обязательно для заполнения и не может быть пустым.')
        return value

    def validate(self, data):
        status = data.get('status')
        if status and status.name.lower() != 'анонс':
            if not data.get('studio'):
                raise serializers.ValidationError({
                    'studio': 'Для не анонсированного аниме студия обязательна'
                })
            if not data.get('director'):
                raise serializers.ValidationError({
                    'director': 'Для не анонсированного аниме директор обязателен'
                })
        return data

    def create(self, validated_data):
        genres = validated_data.pop('genres', [])
        anime = Anime.objects.create(**validated_data)
        anime.genres.set(genres)
        if 'request' in self.context:
            anime.user = self.context['request'].user
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
