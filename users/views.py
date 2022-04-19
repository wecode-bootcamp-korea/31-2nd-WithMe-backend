import jwt, datetime, json, uuid, boto3

from django.views        import View
from django.http         import JsonResponse
from django.conf         import settings
from django.db.models    import Q

from users.models        import User
from users.kakao         import KakaoAPI

from cores.decorator     import login_authorization
from cores.imagehandler  import ImageHandler

from places.models       import Place, PlaceStatus

from withme.settings     import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_REGION


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

class HostMainView(View):
    @login_authorization
    def get(self, request):
        host   = request.GET.get('host', None)
        status = request.GET.get('status', None)
        limit  = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        user   = request.user
        
        q = Q()

        if host:
            q &= Q(host__id = host)

        if status:
            q &= Q(status__id = status)

        places = Place.objects.filter(q)[offset:offset+limit]

        results = [
            {
                'host' : {
                        'nickname'      : user.nickname,
                        'profile_image' : user.profile_image
                    },
                'place' : [{
                    'id'           : place.id,
                    'img_url'      : place.image_url,
                    'title'        : place.title,
                    'subtitle'     : place.subtitle,
                    'price'        : int(place.price),
                    'running_date' : place.running_date
                } for place in places] 
            } 
        ]

        return JsonResponse({'results':results}, status=200)

class HostRegisterView(View):
    @login_authorization
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            hosts, created = Host.objects.get_or_create(
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

            return JsonResponse({'message':'Success'}, status=status)

        except KeyError:
            return JsonResponse({'message':'Key_error'}, status=400)

    @login_authorization
    def get(self, request, host_id):
        try:
            host = Host.objects.get(id = host_id)

            host_info = {
                    'id'           : host.id,
                    'profile_img'  : host.user.profile_image,
                    'nickname'     : host.user.nickname,
                    'introduction' : host.introduction,
                    'bank'         : host.bank,
                    'account'      : host.account
                }

            return JsonResponse({'host_info':host_info}, status=200)

        except Host.DoesNotExist:
            return JsonResponse({'message':'Invalid_host'} , status = 401)

boto3_client = boto3.client(
    's3',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)

class PlaceRegisterView(View):
    @login_authorization
    def post(self, request):
        try:
            image_handler = ImageHandler(boto3_client, AWS_STORAGE_BUCKET_NAME, AWS_REGION)
            post          = request.POST
            user          = request.user
            place_img     = request.FILES.__getitem__('place_img')
            
            running_date  = datetime.datetime.strptime(post['running_date'], '%Y-%m-%d')
            close_date    = datetime.datetime.strptime(post['close_date'], '%Y-%m-%d')
            
            if running_date < datetime.datetime.today():
                return JsonResponse({'message':'Invalid_running_date'}, status=400)

            if close_date < datetime.datetime.today():
                return JsonResponse({'message':'Invalid_close_date'}, status=400)
            
            Place.objects.create(
                title        = post['title'],
                image_url    = image_handler.upload_file(place_img),
                location     = post['location'],
                subtitle     = post['subtitle'],
                price        = post['price'],
                running_date = post['running_date'],
                running_time = post['running_time'],
                max_visitor  = post['max_visitor'],
                preparation  = post['preparation'],
                close_date   = post['close_date'],
                status       = PlaceStatus.objects.get(id=2),
                host         = Host.objects.get(user = user)
            )

            return JsonResponse({'message':'Success'}, status=201)

        except KeyError:
            return JsonResponse({'message':'Key_error'}, status=400)

        except Host.DoesNotExist:
            return JsonResponse({'message':'Invalid_host'}, status=401)


