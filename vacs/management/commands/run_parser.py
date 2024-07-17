from django.core.management import BaseCommand

from vacs.models import City, Vacancy

from parsing.Parser import HHPage, HH_URL


class Command(BaseCommand):
    help = 'Run parser'

    def handle(self, *args, **options):
        page = HHPage(HH_URL)
        page.parser()

        for title, city, url in page.get_list_vacancies():
            vac, vac_obj_created = Vacancy.objects.get_or_create(
                url=url,
                defaults={
                    'title': title
                }
            )

            if vac_obj_created:
                city_obj, city_obj_created = City.objects.get_or_create(name=city)

                vac.city = city_obj
                vac.save()

            print(vac, vac_obj_created)






