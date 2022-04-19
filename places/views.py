from django.views import View
from django.http  import JsonResponse

from places.models import Place, Review
from users.models  import User


class PlaceDetailView(View):
    def get(self, request, place_id):
        try:
            place  = Place.objects.get(id=place_id)

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
                'host': {
                    'host_nickname'      : User.objects.get(id=place.host_id).nickname,
                    'host_profile_image' : User.objects.get(id=place.host_id).profile_image,
                    'host_introduction'  : place.host.introduction
                    },
                'review_list': [{
                    'nickname'     : review.user.nickname,
                    'content'      : review.content,
                    'running_date' : place.running_date,
                } for review in Review.objects.filter(place_id=place_id)]
            }
            return JsonResponse({'result': result}, status=200)

        except Place.DoesNotExist:
            return JsonResponse({'result': 'Place does not exit'}, status=404)
