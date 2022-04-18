from http import client
import json, jwt

from unittest.mock import patch, MagicMock

from django.conf   import settings
from django.conf   import settings
from django.test   import TestCase, Client

from users.models  import *
from places.models import *

class KakaoLoginTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            social_id      = "123123",
            nickname      = "test",
            email         = "test@gmail.com",
            profile_image = "https://ifh.123123/g/ElNIU1.jpg",
        )

    def tearDown(self):
        User.objects.all().delete()
    
class SignInTest(TestCase):
    @patch('users.kakao.requests')
    def test_kakao_signin_view_get_success(self, mocked_requests):
            client = Client()

            class MockedResponse:
                status_code = 200
                
                def json(self):
                    return {
                        "id": 2145645622,
                        "connected_at": "2022-02-16T05:48:20Z",
                        "properties": {
                            "nickname": "test"
                        },
                        "kakao_account": {
                        "profile_nickname_needs_agreement": False,
                        "profile_image_needs_agreement": True,
                        "profile": {
                            "nickname": "test",
                            "thumbnail_image_url": "h123.jpg",
                            "profile_image_url": "h123.jpg",
                            "is_default_image": True
                        },
                        "has_email": True,
                        "email_needs_agreement": False,
                        "is_email_valid": True,
                        "is_email_verified": True,
                        "email": "test@gmail.com",
                        "has_gender": True,
                        }
                    }

            mocked_requests.get = MagicMock(return_value = MockedResponse())
            headers = {"HTTP_Authorization" : "123123"}
            response = client.get("/users/signin", **headers)

            self.assertEqual(response.status_code, 201 | 200) 
            
    @patch('users.kakao.requests')
    def test_kakao_signin_fail_key_error(self, mocked_requests):
        client = Client()
        
        class MockedResponse:
            status_code = 400

            def json(self):
                return {
                    'id' : 2145645622,
                    'kakao_account' : {
                        'profile' : {
                            'nickname' : 'test'
                        }
                    }
                }
        
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'Authorization' : '123123'}
        response            = client.get('/users/signin', **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'Key error'})


    @patch('users.kakao.requests')
    def test_kakao_signin_invaild_token_error(self, mocked_requests):
        client = Client()

        class MockedResponse:
            status_code = 401
            def json(self):
                return {'msg': 'no authentication key!', 'code': -401}
        

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers  = {'Authorizaton' : "Bearer Bearer 1231231231"} 
        response = client.get("/users/signin", **headers)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message' : 'Invalid token'})

class MypageMainTest(TestCase):
    def setUp(self):
        User.objects.bulk_create([
            User( 
                id =1,
                social_id      = "123123",
                nickname      = "test",
                email         = "test@gmail.com",
                profile_image = "https://ifh.123123/g/ElNIU1.jpg",
                point = "0"
            ),
            User( 
                id =2,
                social_id      = "123123",
                nickname      = "asd",
                email         = "asd@gmail.com",
                profile_image = "https://ifh.123123/g/asdElNIU1.jpg",
                point = "0"
            )
        ])
        Host.objects.create(
            id = 1,
            bank = '하나',
            account = '123123123',
            introduction = 'testtest',
            user_id = 1
        )
        PlaceStatus.objects.create(
            id = 1,
            status = True
        )
      
        Place.objects.create(
            id           = 1,
            title        = "test",
            subtitle     = "sub_test",
            price        = "123123",
            running_time = "3",
            running_date = "2022-01-01",
            location     = "선릉",
            preparation  = "test",
            max_visitor  = 4,
            image_url    = "test.jpg",
            close_date   = "2022-03-03",
            status_id    = 1,
            host_id      = 1,
        )
        Reservation.objects.create(
            id =1,
            user_id  = 2,
            place_id = 1
        )


    def tearDown(self):
        User.objects.all().delete()
        Place.objects.all().delete()
        PlaceStatus.objects.all().delete()
        Host.objects.all().delete()

    @patch('users.views')
    def test_mypage_main_get_success(self,mocked_requests):
        client = Client()
        class MockedResponse:
            data = {
                'nickname'     : "test",
                'email'        : "test@gmail.com",
                'profile_image': "https://ifh.123123/g/ElNIU1.jpg",
                'point'        : "0"
            }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        token    = jwt.encode({'user_id':1},settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization" : token}
        
        response = client.get("/users/mypage", **headers)
        self.assertEqual(response.status_code, 200)

    @patch('users.views')
    def test_mypage_main_post_success(self,mocked_requests):
        client = Client()

        data = {
            "place_id": 1
        }

        token    = jwt.encode({'user_id':2},settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization" : token}
        
        response = client.post("/users/mypage",json.dumps(data),content_type='application/json' ,**headers)
        self.assertEqual(response.status_code, 200)

    @patch('users.views')
    def test_point_charge_post_keyerror(self, mocked_requests):
        client = Client()
        
        data = {
            "point"  : 0
        }

        token    = jwt.encode({'user_id':1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization" : token}
        
        response = client.post("/users/mypage/point", json.dumps(data),content_type='application/json' ,**headers)
        self.assertEqual(response.status_code, 200)
        

    @patch('users.views')
    def test_point_charge_post_keyerror(self, mocked_requests):
        client = Client()
        
        data = {
            
        }

        token    = jwt.encode({'user_id':1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization" : token}
        
        response = client.post("/users/mypage/point", json.dumps(data),content_type='application/json' ,**headers)
        self.assertEqual(response.status_code, 400)
        
    @patch('users.views')
    def test_point_charge_post_valueerror(self, mocked_requests):
        client = Client()
        
        data = {
            'point' : '',
        }

        token    = jwt.encode({'user_id':1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization" : token}
        
        response = client.post("/users/mypage/point", json.dumps(data),content_type='application/json' ,**headers)
        self.assertEqual(response.status_code, 401)
        


   
