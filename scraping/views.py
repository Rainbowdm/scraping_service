from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


# Create your views here.

def home_view(request):
    # print(request.GET)
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    query_set = []
    if city or language:
        list_filter = {}
        if city:
            list_filter['city__slug'] = city
        if language:
            list_filter['language__slug'] = language
    query_set = Vacancy.objects.filter(**list_filter)
    # query_set = Vacancy.objects.all()
    return render(request, 'scraping/home.html', {'object_list': query_set, 'form': form})
