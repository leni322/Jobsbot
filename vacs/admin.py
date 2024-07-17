from django.contrib import admin

from vacs.models import City, Vacancy


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
    )


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'city'
    )

    list_filter = (
        'city',
    )

    search_fields = (
        'title',
    )

    raw_id_fields = (
        'city',
    )
