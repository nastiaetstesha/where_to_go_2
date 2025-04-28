import os
import requests
import sys
import time
import requests.exceptions
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from places.models import Place, PlaceImage
from django.core.exceptions import MultipleObjectsReturned


class Command(BaseCommand):
    help = 'Load place data from JSON URL'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str)

    def handle(self, *args, **options):
        response = requests.get(options['json_url'])
        response.raise_for_status()
        raw_place = response.json()

        title = raw_place['title']
        
        try:
            place, created = Place.objects.get_or_create(
                title=title,
                defaults={
                    'short_description': raw_place['description_short'],
                    'long_description': raw_place['long_description'],
                    'latitude': raw_place['coordinates']['lat'],
                    'longitude': raw_place['coordinates']['lng']
                }
            )
        except MultipleObjectsReturned:
            self.stdout.write(
                self.style.ERROR(f'Найдено несколько мест с названием: {title}')
            )
            return

        if not created:
            self.stdout.write(
                self.style.WARNING(f'Место уже существует: {title}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Добавлено новое место: {title}')
            )

        for img_url in raw_place['imgs']:
            try:
                img_response = requests.get(img_url)
                img_response.raise_for_status()

                img_name = os.path.basename(urlparse(img_url).path)
                PlaceImage.objects.create(
                    place=place,
                    image=ContentFile(img_response.content, name=img_name)
                )
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
                print(
                    f'Ошибка при загрузке изображения {img_url}: {e}',
                    file=sys.stderr
                    )
                time.sleep(1)
            except Exception as e:
                print(
                    f'Неизвестная ошибка при обработке {img_url}: {e}',
                    file=sys.stderr
                    )
                time.sleep(1)
