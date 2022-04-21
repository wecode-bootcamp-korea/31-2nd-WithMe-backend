import json

import json

from django.views import View
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Q, F, Count


from places.models import Place, Review, Reservation
from users.models import Host
from cores.decorator import login_authorization


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
                'latitude'     : place.latitude,
                'longitude'    : place.longitude
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


class PlaceReviewListView(View):
    def get(self, request, place_id):
        try:
            place = Place.objects.get(id=place_id)

            result = [{
                        'nickname'     : review.user.nickname,
                        'content'      : review.content,
                        'running_date' : place.running_date,
                    } for review in Review.objects.filter(place_id=place_id)]
            return JsonResponse({'result': result}, status=200)

        except Place.DoesNotExist:
            return JsonResponse({'message': 'Place does not exit'}, status=404)


class PlaceHostInformationView(View):
    def get(self, request, place_id):
        try:

            place = Place.objects.select_related('host').get(id=place_id)
            result = {
                    'host_nickname'      : place.host.user.nickname,
                    'host_profile_image' : place.host.user.profile_image,
                    'host_introduction'  : place.host.introduction
            }
            return JsonResponse({'result': result}, status=200)

        except Place.DoesNotExist:
            return JsonResponse({'message': 'Place does not exit'}, status=404)


class PlaceSearchView(View):
    def get(self, request):
        word = request.GET.get('k', None)

        q = Q()

        if word:
            q &= Q(title__icontains=word)

        places = Place.objects.filter(q)

        result = [{
            'id'       : place.id,
            'img_url'  : place.image_url,
            'title'    : place.title,
            'subtitle' : place.subtitle,
            'location' : place.location,
            'price'    : place.price
        }for place in places]
        return JsonResponse({'result': result}, status=200)


class HostResistPlaceList(View):
    @login_authorization
    def get(sef, request):
        try:
            user = request.user
            host = Host.objects.get(user_id=user.id)

            if not host:
                return JsonResponse({'message': 'You\'are not host'}, status=401)

            places = Place.objects.filter(host_id=host.id)

            hostplace = [{
                "id"           : place.id,
                "title"        : place.title,
                "subtitle"     : place.subtitle,
                "img_url"      : place.image_url,
                "location"     : place.location,
                "closed_date"  : place.close_date,
                "running_date" : place.running_date if place.running_date.strftime("%Y-%m-%d") >= datetime.now()
                                                                         .strftime("%Y-%m-%d") else "is_closed",
            } for place in places]
            return JsonResponse({'results': hostplace}, status=200)

        except AttributeError:
            return JsonResponse({'message': 'None host'}, status=403)


class PlaceReservation(View):
    @login_authorization
    def post(self, request):
        try:
            data     = json.loads(request.body)
            user     = request.user
            place_id = data['place_id']
            place    = Place.objects.get(id=place_id)

            if Host.objects.get(user_id=user.id).id == place.host_id:
                return JsonResponse({'message': 'You are host'}, status=400)

            if Reservation.objects.filter(user_id=user.id, place_id=place_id, place__close_date__gte=datetime.now())\
                                                                                                           .exists():
                return JsonResponse({'message': 'Already exist room'}, status=400)

            if user.point < place.price:
                return JsonResponse({'message': 'Not enough point'}, status=400)
            Reservation.objects.create(
                place_id = place_id,
                user_id  = user.id
            )
            user.point -= Place.objects.get(id=place_id).price
            user.save()
            return JsonResponse({'message': 'Success'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'Key error'}, status=400)


class PlaceListView(View):
    def get(self, request):
        try:
            status      = request.GET.get('status', 'new_place')
            participant = request.GET.get('participant', 'every_place')
            sort        = request.GET.get('sort', 'running_date')

            q = Q()

            if status == "new_place":
                q &= Q(running_date__gt=datetime.now())

            if status == "finished_place":
                q &= Q(running_date__lte=datetime.now())

            place_list = Place.objects.filter(q).order_by(sort)

            if participant == "full_visitor":
                place_list = place_list.annotate(count=Count("reservation__id")).filter(count__gte=F('max_visitor'))\
                                                                                .order_by(sort)

            elif participant == "less_visitor":
                place_list = place_list.annotate(count=Count("reservation__id")).filter(count__lt=F('max_visitor')
                                                                                .order_by(sort))

            else:
                pass

            result = [{
                'id'           : place.id,
                'img_url'      : place.image_url,
                'max_visitor'  : place.max_visitor,
                'title'        : place.title,
                'subtitle'     : place.subtitle,
                'location'     : place.location,
                'running_date' : place.running_date,
                'price'        : place.price
            } for place in place_list]

            return JsonResponse({'result': result}, status=200)

        except KeyError:
            return JsonResponse({'message': 'Key error'}, status=400)

        except TypeError:
            return JsonResponse({'message': 'Type error'}, status=400)

