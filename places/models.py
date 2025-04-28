from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Название', max_length=200, unique=True)
    short_description = models.TextField('Краткое описание', blank=True)
    long_description = HTMLField('Подробное описание', blank=True)
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место'
        )
    image = models.ImageField('Изображение')
    order = models.PositiveIntegerField('Порядок', default=0, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order} — {self.place.title}'
