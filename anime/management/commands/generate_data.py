from django.core.management.base import BaseCommand
from faker import Faker
from random import choice, choices, randint, random
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
            "Masashi Kishimoto", "Eiichiro Oda", "Naoko Takeuchi",
            "Katsuhiro Otomo", "Tatsuya Ishihara", "Yasuhiro Yoshiura", "Mamoru Oshii",
            "Kiyoshi Kurosawa", "Takahiro Omori", "Rintaro", "Shinji Aramaki",
            "Yoko Kanno", "Hiroshi Hamasaki", "Yoshiyuki Sadamoto", "Kenji Kamiyama",
            "Keiichi Sato", "Satoshi Kuwabara", "Yoshikazu Yasuhiko", "Hideki Anno",
            "Isao Takahata", "Hiroshi Noguchi", "Takashi Murakami", "Atsuko Ishizuka",
            "Nobuyuki Takeuchi", "Shuhei Morita", "Kazuya Tsurumaki", "Yoshihiro Nishimura",
            "Makoto Nagahama", "Sakamoto Sato", "Kazuo Sakai", "Kazuki Akane",
            "Yasuhiro Takemoto", "Yuto Kuroda", "Hidetaka Anno", "Kenji Okada",
            "Yun Jun-sik", "Kim Seong-ho", "Zhang Yimou", "Chen Kaige",
            "Ying Xianwen", "Wang Wei", "Xu Anhua", "Yuya Ishii"
        ]

        
        for name in famous_directors:
            director = Director.objects.create(
                name=name,
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
            # Chinese studios
            ('Colored Pencil Animation', 'China'),
            ('B.CMAY PICTURES', 'China'),
            ('Haoliners Animation League', 'China'),
            ('Light Chaser Animation', 'China'),
            ('Nice Boat Animation', 'China'),
            ('Fantawild Animation', 'China'),
            ('Wolf Smoke Studio', 'China'),
            ('Shanghai Animation Film Studio', 'China')
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
            "Naruto", "One Piece", "Dragon Ball", "Attack on Titan",
            "My Hero Academia", "Fullmetal Alchemist", "Death Note", "Sword Art Online",
            "Demon Slayer", "Tokyo Ghoul", "Bleach", "Fairy Tail",
            "Re:Zero", "One Punch Man", "Fate", "Neon Genesis Evangelion",
            "Hunter x Hunter", "JoJo's Bizarre Adventure", "Naruto Shippuden", "Attack on Titan",
            "Cowboy Bebop", "Gintama", "Yu Yu Hakusho", "Trigun",
            "The Promised Neverland", "Steins;Gate", "Mob Psycho 100", "Black Clover",
            "Tokyo Revengers", "Your Name", "Kaguya-sama", "Code Geass",
            "D.Gray-man", "Akame ga Kill!", "Inuyasha", "Bleach",
            "Clannad", "Monogatari", "Angel Beats!", "Mob Psycho 100",
            "Hellsing", "Fruits Basket", "Black Lagoon", "Highschool of the Dead",
            "Elfen Lied", "Neon Genesis Evangelion", "Spice and Wolf", "Cowboy Bebop",
            "Angel Beats!", "Toradora!", "Bleach", "Naruto",
            "Fate", "Naruto", "The Seven Deadly Sins", "Assassination Classroom",
            "Bleach", "Fairy Tail", "Tokyo Ghoul", "Dragon Ball",
            "JoJo's Bizarre Adventure", "Sword Art Online", "The Rising of the Shield Hero", "No Game No Life",
            "Attack on Titan", "Overlord", "Re:Zero", "Violet Evergarden",
            "Made in Abyss", "Psycho-Pass", "Hunter x Hunter", "K-On!",
            "Fairy Tail", "Tokyo Ghoul", "Beastars", "Great Teacher Onizuka",
            "Hachimitsu to Clover", "K-On!", "Attack on Titan", "Code Geass",
            "Bleach", "Fate", "No Game No Life", "InuYasha",
            "Tengen Toppa Gurren Lagann", "Nodame Cantabile", "Detective Conan", "JoJo's Bizarre Adventure",
            "Angel Beats!", "Dragon Ball", "Black Clover", "Yu-Gi-Oh!",
            "JoJo's Bizarre Adventure"
        ]

        weights = []
        for status in statuses:
            if status.name == 'Анонс':
                weights.append(0.1)  # Низкий шанс для 'Анонс'
            elif status.name == 'Вышел':
                weights.append(0.6)
            else:
                weights.append(0.3)  
        
        for i in range(len(anime_titles)):
            status = choices(statuses, weights=weights, k=1)[0]
            
            if status.name == 'Анонс':
                date = None
                if random() > 0.8:  # 90% шанс что будет студия/директор
                    studio = choice(studios)
                    director = choice(directors)
                else:
                    studio = None
                    director = None
            else:
                date = fake.date_between(start_date='-30y', end_date='now')
                studio = choice(studios)
                director = choice(directors)

            title = anime_titles[i]  # Берем только название из существующего списка

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