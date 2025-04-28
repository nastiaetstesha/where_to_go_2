from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse 
from .models import Place


def show_main_page(request):
    return render(request, 'start_page.html')


def place_detail(request, place_id):
    place = get_object_or_404(
        Place.objects.prefetch_related('images'),
        id=place_id
    )
    images = [image.image.url for image in place.images.all()]

    serialized_place = {
        'title': place.title.strip('"'),
        'imgs': images,
        'short_description': place.short_description,
        'long_description': place.long_description,
        'coordinates': {
            'lng': place.longitude,
            'lat': place.latitude,
        }
    }

    return JsonResponse(
        serialized_place,
        json_dumps_params={
            'ensure_ascii': False,
            'indent': 2
        }
    )


def places_geojson(request):
    places = Place.objects.only('id', 'title', 'longitude', 'latitude')
    features = []

    for place in places:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.longitude, place.latitude], 
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": reverse('place_detail', args=[place.id])
            }
        })

    return JsonResponse({
        "type": "FeatureCollection",
        "features": features
    })
