from django.views import View
from django.http import JsonResponse
from datetime import datetime

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


class MainPlaceListView(View):
    def get(self, request):
        place_list_1 = Place.objects.filter().order_by('-created_at')[0:4]
        place_list_2 = Place.objects.filter().order_by('price')[0:4]
        place_list_3 = Place.objects.filter(running_date__gt=datetime.now()).order_by('running_date')[0:4]

        result = [{
            'id'           : place.id,
            'img_url'      : place.image_url,
            'title'        : place.title,
            'subtitle'     : place.subtitle,
            'location'     : place.location,
            'running_date' : place.running_date,
            'price'        : place.price
        } for place in place_list_1]

        second_result = [{
            'id'           : place.id,
            'img_url'      : place.image_url,
            'title'        : place.title,
            'subtitle'     : place.subtitle,
            'location'     : place.location,
            'running_date' : place.running_date,
            'price'        : place.price
        } for place in place_list_2]

        third_result = [{
            'id'           : place.id,
            'img_url'      : place.image_url,
            'title'        : place.title,
            'subtitle'     : place.subtitle,
            'location'     : place.location,
            'running_date' : place.running_date,
            'price'        : place.price
        } for place in place_list_3]

        return JsonResponse({'create_time': result, 'low_price': second_result,
                             'running_date': third_result}, status=200)

