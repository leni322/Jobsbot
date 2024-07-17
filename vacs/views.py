from django.views.generic.list import ListView

from vacs.models import Vacancy


# Create your views here.
class VacancyList(ListView):
    model = Vacancy
    template_name = 'vacs/vacancy_list.html'

