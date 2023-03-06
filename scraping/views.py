from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from .forms import FindForm
from .models import Vacancy


# Create your views here.

def home_view(request):
    # print(request.GET)
    form = FindForm()

    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
    # print(request.GET)
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    context = {'city': city, 'language': language, 'form': form}
    if city or language:
        list_filter = {}
        if city:
            list_filter['city__slug'] = city
        if language:
            list_filter['language__slug'] = language

        query_set = Vacancy.objects.filter(**list_filter).select_related('city', 'language')
        paginator = Paginator(query_set, 10)  # Show 10 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping/list.html', context)


def v_detail(request, pk=None):
    # object_ = Vacancy.objects.get(pk=pk)
    object_ = get_object_or_404(Vacancy, pk=pk)
    return render(request, 'scraping/detail.html', {'object': object_})


class VDetail(DetailView):
    queryset = Vacancy.objects.all()
    template_name = 'scraping/detail.html'
    context_object_name = 'object'


class VList(ListView):
    model = Vacancy
    template_name = 'scraping/list.html'
    form = FindForm()
    paginate_by = 2

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        context['form'] = self.form
        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        if city or language:
            list_filter = {}
            if city:
                list_filter['city__slug'] = city
            if language:
                list_filter['language__slug'] = language
            query_set = Vacancy.objects.filter(**list_filter).select_related('city', 'language')
        return query_set
