from django.db import models

class Country(models.Model):
    name = models.TextField("Страна")

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self) -> str:
        return self.name

class Studio(models.Model):
    name = models.TextField("Название студии")
    country = models.ForeignKey("Country", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Студия"
        verbose_name_plural = "Студии"

    def __str__(self) -> str:
        return self.name


class Director(models.Model):
    name = models.TextField("Имя директора")

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
    date = models.TextField("Дата выпуска")
    studio = models.ForeignKey("Studio", on_delete=models.CASCADE, null=True)
    director = models.ForeignKey("Director", on_delete=models.SET_NULL, null=True)
    genres = models.ManyToManyField("Genre", verbose_name="Жанры")
    status = models.ForeignKey("Status", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Аниме"
        verbose_name_plural = "Анимешки"

    def __str__(self) -> str:
        return self.title_name


