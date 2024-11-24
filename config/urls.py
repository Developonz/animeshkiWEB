from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from anime.views import AnimeViewSet, GenreViewSet, StudioViewSet, DirectorViewSet, StatusViewSet, CountryViewSet

router = DefaultRouter()
router.register("animes", AnimeViewSet)
router.register("genres", GenreViewSet)
router.register("studios", StudioViewSet)
router.register("directors", DirectorViewSet)
router.register("statuses", StatusViewSet)
router.register("countries", CountryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 