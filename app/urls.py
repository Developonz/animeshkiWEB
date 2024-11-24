from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from anime.api import AnimeViewSet, GenreViewSet, StudioViewSet, DirectorViewSet, StatusViewSet, CountryViewSet
from anime.views import ShowAnimesView
from django.conf.urls.static import static
from django.conf import settings

# Создаем роутер и регистрируем вьюсеты
router = DefaultRouter()
router.register(r'animes', AnimeViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'studios', StudioViewSet)
router.register(r'directors', DirectorViewSet)
router.register(r'statuses', StatusViewSet)
router.register(r'countries', CountryViewSet)


urlpatterns = [
    path('', ShowAnimesView.as_view(), name='home'), 
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
