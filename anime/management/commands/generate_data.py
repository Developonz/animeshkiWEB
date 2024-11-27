from django.core.management.base import BaseCommand
from faker import Faker
from random import choice, randint, random
from datetime import datetime, timedelta

from anime.models import Director, Studio, Anime, Country, Genre, Status

# Константы для количества генерируемых записей
DIRECTORS_COUNT = 1000
ANIME_COUNT = 1000

class Command(BaseCommand):

    def handle(self, *args, **options):
        fake = Faker(['en_US'])
        
        # Получаем существующие данные
        countries = list(Country.objects.all())
        genres = list(Genre.objects.all())
        statuses = list(Status.objects.all())
        
        self.stdout.write('Создаём директоров...')
        directors = []
        famous_directors = [
            "Hayao Miyazaki", "Makoto Shinkai", "Hideaki Anno", 
            "Satoshi Kon", "Mamoru Hosoda", "Masaaki Yuasa",
            "Shinichiro Watanabe", "Hiroyuki Imaishi", "Kunihiko Ikuhara",
            "Yoshiyuki Tomino", "Gen Urobuchi", "Tetsuro Araki",
            "Masashi Kishimoto", "Eiichiro Oda", "Naoko Takeuchi"
        ]
        
        for name in famous_directors:
            director = Director.objects.create(
                name=name,
                picture=None
            )
            directors.append(director)
        
        for i in range(DIRECTORS_COUNT - len(famous_directors)):
            director = Director.objects.create(
                name=f"{fake.first_name()} {fake.last_name()}",
                picture=None
            )
            directors.append(director) 
            
        self.stdout.write('Создаём студии...')
        studios = []
        studio_data = [
            # Japanese studios
            ('Studio Ghibli', 'Japan'),
            ('Kyoto Animation', 'Japan'),
            ('Madhouse', 'Japan'),
            ('Bones', 'Japan'),
            ('Production I.G', 'Japan'),
            ('MAPPA', 'Japan'),
            ('ufotable', 'Japan'),
            ('Sunrise', 'Japan'),
            ('Toei Animation', 'Japan'),
            ('White Fox', 'Japan'),
            # Korean studios
            ('Studio Mir', 'Korea'),
            ('SAMG Animation', 'Korea'),
            ('MOI Animation', 'Korea'),
            ('Sunwoo Entertainment', 'Korea'),
            ('DR Movie', 'Korea'),
            ('JM Animation', 'Korea'),
            ('Dong Woo Animation', 'Korea'),
            ('Rough Draft Korea', 'Korea'),
            ('Studio Animal', 'Korea'),
            ('EMK Musical Company', 'Korea'),
            # Chinese studios
            ('Colored Pencil Animation', 'China'),
            ('B.CMAY PICTURES', 'China'),
            ('Haoliners Animation League', 'China'),
            ('Light Chaser Animation', 'China'),
            ('Nice Boat Animation', 'China'),
            ('Fantawild Animation', 'China'),
            ('Wolf Smoke Studio', 'China'),
            ('Shanghai Animation Film Studio', 'China'),
            ('Feitong Cartoon', 'China'),
            ('Youku Animation', 'China')
        ]
        
        for name, country_name in studio_data:
            country = next((c for c in countries if c.name == country_name), countries[0])
            studio = Studio.objects.create(
                name=name,
                picture=None,
                country=country
            )
            studios.append(studio)

        self.stdout.write('Создаём аниме...')
        anime_titles = [
            "Sword Art Online", "Attack on Titan", "One Punch Man", "My Hero Academia",
            "Death Note", "Fullmetal Alchemist", "Demon Slayer", "Tokyo Ghoul",
            "Steins;Gate", "Code Geass", "Hunter x Hunter", "Black Clover",
            "Naruto", "Bleach", "One Piece", "Dragon Ball", "JoJo's Bizarre Adventure",
            "Neon Genesis Evangelion", "Cowboy Bebop", "Ghost in the Shell",
            "Your Name", "Spirited Away", "Princess Mononoke", "Akira", "A Silent Voice"
        ]
        
        for i in range(ANIME_COUNT):
            status = choice(statuses)
            if status.name == 'Анонс':
                date = None
                if random() > 0.7:  # 30% шанс что будет студия/директор
                    studio = choice(studios)
                    director = choice(directors)
                else:
                    studio = None
                    director = None
            else:
                date = fake.date_between(start_date='-30y', end_date='now')
                studio = choice(studios)
                director = choice(directors)

            if i < len(anime_titles):
                title = anime_titles[i]
            else:
                prefix = choice(["Super ", "Magical ", "Divine ", "Epic ", "Legendary ", ""])
                suffix = choice([" Story", " Chronicles", " Adventure", " Tales", " Saga", ""])
                middle = fake.catch_phrase().replace(".", "").replace(",", "")
                title = f"{prefix}{middle}{suffix}"

            # Подготавливаем жанры заранее
            selected_genres = fake.random_elements(
                elements=genres,
                length=randint(2, 5),
                unique=True
            )

            # Создаем объект аниме со всеми необходимыми полями
            anime = Anime.objects.create(
                title_name=title,
                status=status,
                date=date,
                studio=studio,
                director=director,
                picture=None,
            )
            # Сразу же устанавливаем жанры
            anime.genres.set([g.id for g in selected_genres])

        self.stdout.write(self.style.SUCCESS('Данные успешно сгенерированы!'))