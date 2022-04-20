import jwt, datetime, json
from django.views import View
from django.http  import HttpResponse, JsonResponse
from django.db.models import Q

from users.models        import User,Host
from places.models       import *
from django.conf         import settings
from cores.decorator     import login_authorization
from users.kakao         import KakaoAPI

from cores.decorator    import login_authorization

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

class UserInfomation(View):
    @login_authorization
    def get(self,request):
        user = request.user
        
        user_info = {
                "nickname" : user.nickname,
                "email"    : user.email,
                "point"    : user.point,
                "profile_image" : user.profile_image,
            }
            
        return JsonResponse({'user_info' : user_info}, status = 200)

class ReservationView(View):
    @login_authorization
    def get (self, request):
        user = request.user
 
        reservation_queryset = Reservation.objects.select_related('place').filter(user = user)

        reservation_list = [{
            "place_id" : reservation.place.id,
            "title"       : reservation.place.title,
            "sub_title"   : reservation.place.subtitle,
            "image"       : reservation.place.image_url,
            "running_date": reservation.place.running_date if reservation.place.running_date >= datetime.date.today() else  f"{reservation.place.running_date} is_closed",
            "location"    : reservation.place.location
        }for reservation in reservation_queryset]
        
        return JsonResponse({'reservation_list':reservation_list}, status = 200)

        
class ReviewView(View):
    @login_authorization
    def post(self, request):
        user = request.user
        data = json.loads(request.body)
        
        review , state = Review.objects.get_or_create(
            user_id  = user.id,
            place_id = Place.objects.get(title = data['title']).id,
            defaults = {"content"  : data['review']}
        )
        if not data['review']:
            return JsonResponse({'message' : 'Key error'}, status=400) 

        if not state:
            review.content = data['review']
            review.save()

        status =  201 if state else 200

        return HttpResponse(status)

    @login_authorization
    def get(self, request):
        user = request.user
        
        q  = Q(place__running_date__lte = datetime.date.today()) & Q(user_id = user.id) 

        reservation_queryset = Reservation.objects.prefetch_related('place').filter(q)

        result = [{
            "id"          : reservation.id,
            "running_date": reservation.place.running_date,
            "title"       : reservation.place.title,
            "sub_title"   : reservation.place.subtitle,
            "image"       : reservation.place.image_url,
            "review"      : [review.content for review in Review.objects.filter(place_id=reservation.place_id, user_id = user.id)]
        }for reservation in reservation_queryset]

        return JsonResponse({'review' : result}, status = 200)

class PointChargeView(View):
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

class HostView(View):
    @login_authorization
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            hosts, created = Host.objects.update_or_create(
                user     = user,
                defaults = {
                    'introduction' : data['introduction'],
                    'bank'         : data['bank'],
                    'account'      : data['account']
                }
            )

            if not created:
                hosts.introduction = data['introduction']
                hosts.bank = data['bank']
                hosts.account = data['account']
                hosts.save()
            
            status = 201 if created else 200

            return JsonResponse({'message':'Success'}, status=201)

        except KeyError:
            return JsonResponse({'message':'Key_error'}, status=400)