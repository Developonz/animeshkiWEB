from anime.models import Anime
from django.views import View
from django.http import HttpResponse

# Create your views here.
class ShowStudentsView(View):
    def get(request, *args, **kwargs):
        animes = Anime.objects.all()
        result = ""
        for s in animes:
            result += s.title_name + "<brs"
        return HttpResponse(result)

