from django.db import models
from django.core.exceptions import ValidationError
import os

class Country(models.Model):
    name = models.TextField("Страна")
    picture = models.ImageField("Изображение", null=True, upload_to="countries")

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self) -> str:
        return self.name

class Studio(models.Model):
    name = models.TextField("Название студии")
    country = models.ForeignKey("Country", on_delete=models.CASCADE, null=True)
    picture = models.ImageField("Изображение", null=True, upload_to="studios")

    class Meta:
        verbose_name = "Студия"
        verbose_name_plural = "Студии"

    def __str__(self) -> str:
        return self.name


class Director(models.Model):
    name = models.TextField("Имя директора")
    picture = models.ImageField("Изображение", null=True, upload_to="directors")

    class Meta:
        verbose_name = "Директор"
        verbose_name_plural = "Директора"

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.TextField("Название жанра")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self) -> str:
        return self.name


class Status(models.Model):
    name = models.TextField("Статус")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self) -> str:
        return self.name


class Anime(models.Model):
    title_name = models.TextField("Название аниме")
    status = models.ForeignKey("Status", on_delete=models.CASCADE, null=False)
    date = models.DateField("Дата выпуска", blank=True, null=True)
    studio = models.ForeignKey("Studio", on_delete=models.SET_NULL, null=True)
    director = models.ForeignKey("Director", on_delete=models.SET_NULL, null=True)
    genres = models.ManyToManyField("Genre", verbose_name="Жанры")
    picture = models.ImageField(upload_to='anime_pictures/', null=True, blank=True)
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Аниме"
        verbose_name_plural = "Анимешки"

    @property
    def username(self):
        return self.user.username if self.user else '-'

    def __str__(self) -> str:
        return self.title_name

    def clean(self):
        errors = {}
        # Ensure that status is set
        if not self.status:
            errors['status'] = 'Поле статус обязательно для заполнения.'

        # Fetch the actual Status instance if necessary
        if isinstance(self.status, int):
            try:
                self.status = Status.objects.get(pk=self.status)
            except Status.DoesNotExist:
                errors['status'] = 'Указан неверный статус.'

        # Check if status is not "Анонс"
        if self.status and self.status.name != 'Анонс':
            # Enforce required fields
            if not self.date:
                errors['date'] = 'Поле дата выпуска обязательно для заполнения.'
            if not self.studio:
                errors['studio'] = 'Поле студия обязательно для заполнения.'
            if not self.director:
                errors['director'] = 'Поле директор обязательно для заполнения.'
        if errors:
            raise ValidationError(errors)
