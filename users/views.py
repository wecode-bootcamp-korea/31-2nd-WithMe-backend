import jwt, datetime
from json.decoder import JSONDecodeError

from django.views import View
from django.http  import JsonResponse
from django.conf  import settings

from users.models import User
from users.kakao  import KakaoAPI

class KaKaoLoginView(View):
    def get(self, request):
        try:
            kakao_token = request.headers.get('Authorization')

            kakao_user  = KakaoAPI(kakao_token).kakao_user()
            
        except KeyError: 
            return JsonResponse({'message' : 'Key error'}, status=400)  

        except JSONDecodeError: 
            return JsonResponse({'message' : 'Json decode error'}, status=400)
    
        user , state = User.objects.get_or_create(
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
            'login_user_id': user.id,
            'exp'          : datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }

        new_token = jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

        return JsonResponse({'new_token' : new_token}, status = status)
