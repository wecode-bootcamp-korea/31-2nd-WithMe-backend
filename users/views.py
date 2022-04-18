import jwt, datetime, json
from django.views import View
from django.http  import HttpResponse, JsonResponse
from django.db.models import Q

from users.models        import User,Host
from places.models       import *
from django.conf         import settings
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

class ReviewView(View):
    @login_authorization
    def post(self, request):
        user = request.user
        data = json.loads(request.body)
        
        reviews , state = Review.objects.get_or_create(
            user_id  = user.id,
            place_id = Place.objects.get(title = data['title']).id,
            defaults = {"content"  : data['review']}
        )
        if not data['review']:
            return JsonResponse({'message' : 'Key error'}, status=400) 
        if not state:

            reviews.content = data['review']
            reviews.save()

        status =  201 if state else 200

        return HttpResponse(status)

    @login_authorization
    def get(self, request):
        user = request.user
        
        q  = Q(place__running_date__lte = datetime.date.today()) & Q(user_id = user.id) 

        reservation_queryset = Reservation.objects.prefetch_related('place').filter(q)

        result = [{
            "id" : reservation.id,
            "running_date" : reservation.place.running_date,
            "title" : reservation.place.title,
            "sub_title" : reservation.place.subtitle,
            "image" : reservation.place.image_url,
            "review": [review.content for review in Review.objects.filter(place_id=reservation.place_id, user_id = user.id)]
        }for reservation in reservation_queryset]

        return JsonResponse({'review' : result}, status = 200)