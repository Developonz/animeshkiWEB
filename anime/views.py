from anime.models import Anime
from django.views.generic import TemplateView
from typing import Any

# Create your views here.
class ShowAnimesView(TemplateView):
    template_name = "animes/show_animes.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['animes'] = Anime.objects.all()
        return context
