from django.views import View
from django.http import JsonResponse

from places.models import Place


class PlaceInformationView(View):
    def get(self, request, place_id):
        try:
            place = Place.objects.get(id=place_id)

            result = {
                'id'           : place.id,
                'title'        : place.title,
                'image_url'    : place.image_url,
                'subtitle'     : place.subtitle,
                'running_date' : place.running_date,
                'location'     : place.location,
                'max_visitor'  : place.max_visitor,
                'running_time' : place.running_time,
                'price'        : place.price,
                'preparation'  : place.preparation,
            }
            return JsonResponse({'result': result}, status=200)

        except Place.DoesNotExist:
            return JsonResponse({'message': 'Place does not exit'}, status=404)