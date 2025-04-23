import os
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = 'Load place data from JSON URL'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str)

    def handle(self, *args, **options):
        response = requests.get(options['json_url'])
        response.raise_for_status()
        data = response.json()

        title = data['title']
        place, created = Place.objects.get_or_create(
            title=title,
            defaults={
                'description_short': data['description_short'],
                'description_long': data['description_long'],
                'latitude': data['coordinates']['lat'],
                'longitude': data['coordinates']['lng']
            }
        )

        if not created:
            self.stdout.write(
                self.style.WARNING(f'Место уже существует: {title}')
                )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Добавлено новое место: {title}')
                )

        for img_url in data['imgs']:
            img_response = requests.get(img_url)
            img_response.raise_for_status()

            img_name = os.path.basename(urlparse(img_url).path)
            image = PlaceImage(place=place)
            image.image.save(
                img_name,
                ContentFile(img_response.content),
                save=True
                )
