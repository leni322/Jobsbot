from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f'{self.name}'



class Vacancy(models.Model):
    title = models.CharField(max_length=128)
    url = models.CharField(max_length=2048)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, default=None)