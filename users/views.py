import jwt, datetime, json

from django.views import View
from django.http  import HttpResponse, JsonResponse
from django.db.models import Q
from django.conf         import settings

from users.models        import User
from places.models       import *

from cores.decorator     import login_authorization
from users.kakao         import KakaoAPI

class KakaoLoginView(View):
    def get(self, request):
        try:
            acces_token = request.headers.get('Authorization')
            kakao_user  = KakaoAPI(acces_token).kakao_user()

            if kakao_user.get('code') == -401: 
                return JsonResponse({'message' : 'Invalid token'}, status=401)

            user, state = User.objects.get_or_create(
                social_id     = kakao_user['id'],
                email         = kakao_user['kakao_account']['email'],
                nickname      = kakao_user['properties']['nickname'],
                defaults={'profile_image': kakao_user['kakao_account']['profile'].get('profile_image_url', None)}
            )

            if not state:
                user.profile_image = kakao_user['kakao_account']['profile'].get('profile_image_url', None)
                user.save()

            status = 200 if not state else 201
            
            payload={
                'user_id': user.id,
                'exp'          : datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }

            new_token = jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

            return JsonResponse({'new_token' : new_token}, status = status)
            
        except KeyError: 
            return JsonResponse({'message' : 'Key error'}, status=400)      


class MypageView(View):
    @login_authorization
    def get (self, request):
        user = request.user
 
        reservations = Reservation.objects.filter(user = user.id).select_related('place')

        result = {
            "nickname" : user.nickname,
            "email"    : user.email,
            "point"    : user.point,
            "profile_image" : user.profile_image,
            "reservation_list" : [{
                "place_id" : reservation.place.id,
                "title"       : reservation.place.title,
                "sub_title"   : reservation.place.subtitle,
                "image"       : reservation.place.image_url,
                "running_date": reservation.place.running_date if reservation.place.running_date >= datetime.date.today() else "is_closed",
                "location"    : reservation.place.location
            }for reservation in reservations]
        }
        
        return JsonResponse({'result':result}, status = 200)

    @login_authorization
    def post(self, request):
        user = request.user
        data = json.loads(request.body)
        res = Reservation.objects.get(place_id = data['place_id'], user_id = user.id)
        res.delete()
        price = Place.objects.get(id = data['place_id']).price
        user.point += price
        user.save()
        
        return HttpResponse(status=200)

class PointView(View):
    @login_authorization
    def post(self, request):
        try:
            user = request.user
            data = json.loads(request.body)
            point = data['point']
            user.point += abs(int(point))
            user.save()

            return JsonResponse({'point':user.point} ,status = 200)

        except KeyError:
            return JsonResponse({'message' : 'Key error'}, status=400)     

        except ValueError:
            return JsonResponse({'message' : 'Value Error'}, status=401)

class ReviewView(View):
    @login_authorization
    def post(self, request):
        user = request.user
        data = json.loads(request.body)

        if not data['review']:
            return JsonResponse({'message' : 'Key error'}, status=400) 

        if not data['title']:
            return JsonResponse({'message' : 'Does not exist'}, status=401) 

        reviews , state = Review.objects.get_or_create(
            user_id  = user.id,
            place_id = Place.objects.get(title = data['title']).id,
            defaults = {"content"  : data['review']}
        )

        if not state:
            reviews.content = data['review']
            reviews.save()

        status =  201 if state else 200

        return HttpResponse(status)

    @login_authorization
    def get(self, request):
        user = request.user
        q  = Q(place__running_date__lte = datetime.date.today()) & Q(user_id = user.id) 
        reservations = Reservation.objects.filter(q)

        result = [{
            "id" : reservation.id,
            "running_date" : reservation.place.running_date,
            "title" : reservation.place.title,
            "sub_title" : reservation.place.subtitle,
            "image" : reservation.place.image_url,
            "review": [review.content for review in Review.objects.filter(place_id=reservation.place_id)]
        }for reservation in reservations]

        return JsonResponse({'review' : result}, status = 200)
