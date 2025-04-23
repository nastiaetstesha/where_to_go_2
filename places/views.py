from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse 
from .models import Place


def show_main_page(request):
    return render(request, 'start_page.html')


def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    images = [image.image.url for image in place.images.all()]

    place_data = {
        'title': place.title.strip('"'),
        'imgs': images,
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lng': place.longitude,
            'lat': place.latitude,
        }
    }

    return JsonResponse(
        place_data,
        json_dumps_params={
            'ensure_ascii': False,
            'indent': 2
        }
    )


def places_geojson(request):
    features = []

    for place in Place.objects.all():
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
