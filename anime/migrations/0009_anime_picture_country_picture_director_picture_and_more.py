# Generated by Django 5.1 on 2024-11-06 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0008_alter_anime_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='picture',
            field=models.ImageField(null=True, upload_to='animes', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='country',
            name='picture',
            field=models.ImageField(null=True, upload_to='countries', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='director',
            name='picture',
            field=models.ImageField(null=True, upload_to='directors', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='studio',
            name='picture',
            field=models.ImageField(null=True, upload_to='studios', verbose_name='Изображение'),
        ),
    ]