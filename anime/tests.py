from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker
from anime.models import Anime, Studio, Director, Genre, Status
from datetime import date

class AnimeViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_anime_list(self):
        # Создаем несколько объектов Anime
        animes = baker.make('anime.Anime', 5)

        # Получаем список объектов через API
        response = self.client.get('/api/animes/')
        data = response.json()

        # Проверяем, что количество объектов совпадает
        assert len(data) == 5

        # Проверяем, что данные из ответа совпадают с данными в базе
        for i in range(5):
            assert animes[i].id == data[i]['id']
            assert animes[i].title_name == data[i]['title_name']


    def test_create_anime(self):
        studio = baker.make('anime.Studio')
        director = baker.make('anime.Director')
        genre = baker.make('anime.Genre')
        anime_status = baker.make('anime.Status', name="Вышел")

        anime_data = {
            "title_name": "Test Anime",
            "date": date.today().isoformat(),
            "studio": studio.id,
            "director": director.id,
            "genres": [genre.id],
            "status": anime_status.id
        }
        
        r = self.client.post('/api/animes/', anime_data, format='json')
        
        # Проверяем, что статус ответа - 201
        assert r.status_code == status.HTTP_201_CREATED, f"Unexpected status code: {r.status_code}"
        
        # Печатаем данные ответа для отладки
        print("Response data:", r.json())
        
        # Проверяем, что ключ 'id' присутствует в ответе
        assert 'id' in r.json(), "Response JSON does not contain 'id'"
        
        new_anime_id = r.json()['id']
        animes = Anime.objects.all()
        assert len(animes) == 1
        new_anime = Anime.objects.filter(id=new_anime_id).first()
        
        assert new_anime.title_name == 'Test Anime'
        assert new_anime.date == date.today()  # Используем date.today() без .isoformat()
        assert new_anime.studio == studio
        assert list(new_anime.genres.all()) == [genre]  # Исправляем проверку на список жанров
        assert new_anime.status == anime_status


    def test_delete_anime(self):
        # Создаем 10 объектов Anime с использованием baker
        animes = baker.make('anime.Anime', 10)

        # Проверяем, что в базе данных 10 объектов
        response = self.client.get('/api/animes/')
        data = response.json()
        assert len(data) == 10

        # Удаляем один из объектов, например, четвертый
        anime_id_to_delete = animes[3].id
        self.client.delete(f'/api/animes/{anime_id_to_delete}/')

        # Проверяем, что в базе данных осталось 9 объектов
        response = self.client.get('/api/animes/')
        data = response.json()
        assert len(data) == 9

        # Проверяем, что удаленного объекта больше нет в списке
        assert anime_id_to_delete not in [anime['id'] for anime in data]



    def test_update_anime(self):
        # Создаем 10 объектов Anime с использованием baker и добавляем жанры
        animes = baker.make('anime.Anime', 10)
        for anime in animes:
            genre = baker.make('anime.Genre')
            anime.genres.add(genre) 

        anime = animes[2]

        # Подготовка данных для обновления
        updated_data = {
            "title_name": "Updated Anime Title",
            "date": anime.date.isoformat() if anime.date else None,
            "studio": anime.studio.id if anime.studio else None,
            "director": anime.director.id if anime.director else None,
            "genres": [genre.id for genre in anime.genres.all()],
            "status": anime.status.id if anime.status else None
        }

        # Выполняем запрос на обновление
        response = self.client.put(f'/api/animes/{anime.id}/', updated_data, format='json')
        assert response.status_code == 200

        # Проверяем, что объект в базе данных обновился
        anime.refresh_from_db()
        assert anime.title_name == "Updated Anime Title"




