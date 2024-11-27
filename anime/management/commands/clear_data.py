from django.core.management.base import BaseCommand
from anime.models import Anime, Director, Studio

class Command(BaseCommand):
    help = 'Очищает данные аниме, директоров и студий из базы данных'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем очистку данных...')
        

        anime_count = Anime.objects.count()
        Anime.objects.all().delete()
        self.stdout.write(f'Удалено {anime_count} записей аниме')
        
        # Очищаем директоров
        director_count = Director.objects.count()
        Director.objects.all().delete()
        self.stdout.write(f'Удалено {director_count} директоров')
        
        # Очищаем студии
        studio_count = Studio.objects.count()
        Studio.objects.all().delete()
        self.stdout.write(f'Удалено {studio_count} студий')
        
        self.stdout.write(self.style.SUCCESS('Данные успешно очищены!')) 