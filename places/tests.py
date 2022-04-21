import jwt

from django.test import TestCase, Client
from datetime import datetime
from django.db.models import Q, F, Count

from places.models import Place, PlaceStatus, Reservation, Review
from users.models import User, Host
from withme import settings


class PlaceInformationTest(TestCase):
    def setUp(self):
        User.objects.create(
            id=1,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            nickname='이산',
            email='dltks@gmail.com',
            social_id=1,
            profile_image='http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_640x640.jpg',
            point=100000.00
        )

        PlaceStatus.objects.create(
            id=1,
            status=False
        )

        Host.objects.create(
            id=1,
            created_at='2022-14-15',
            updated_at='2022-14-15',
            bank='다이아',
            account='1111-1111-1111',
            introduction='안녕',
            user_id=1
        )

        Place.objects.create(
            id=1,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='로컨 에너테인먼트의 모든것',
            subtitle='집에서 만끽하는 편안함',
            price=25000.00,
            running_time=2,
            running_date='2022-04-01',
            location='포항',
            preparation='닌텐도 스위치',
            max_visitor=10,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/andrew-varnum-uNKyYp616wo-unsplash.jpg',
            close_date='2022-03-25',
            latitude=36.0076820000,
            longitude=129.3332720000,
            host_id=1,
            status_id=1
        )

    def tearDown(self):
        User.objects.all().delete()
        PlaceStatus.objects.all().delete()
        Host.objects.all().delete()
        Place.objects.all().delete()

    def test_success_place_information_with_get_method(self, place_id=1):
        client   = Client()
        response = client.get(f'/places/placeinformation/{place_id}')

        place    = Place.objects.get(id=place_id)

        self.assertEqual(response.json(), {
                'result': {
                    'id'           : place.id,
                    'title'        : place.title,
                    'image_url'    : place.image_url,
                    'subtitle'     : place.subtitle,
                    'running_date' : place.running_date.strftime("%Y-%m-%d"),
                    'location'     : place.location,
                    'max_visitor'  : place.max_visitor,
                    'running_time' : place.running_time,
                    'price'        : str(place.price),
                    'preparation'  : place.preparation,
                    'latitude': place.latitude,
                    'longitude': place.longitude
                    }
                }
            )
        self.assertEqual(response.status_code, 200)

    def test_fail_place_does_not_exist_error_with_get_method(self, place_id=35):
        client   = Client()
        response = client.get(f'/places/placeinformation/{place_id}')

        self.assertEqual(response.json(), {
                    'message': 'Place does not exit'
                }
            )

        self.assertEqual(response.status_code, 404)


class MainPlaceListTest(TestCase):
    def setUp(self):
        User.objects.create(
            id=1,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            nickname='이산',
            email='dltks@gmail.com',
            social_id=1,
            profile_image='http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_640x640.jpg',
            point=90500.00
        )


class PlaceListTest(TestCase):
    def setUp(self):
        User.objects.create(
            id=1,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            nickname='이산',
            email='dltks@gmail.com',
            social_id=1,
            profile_image='asdfasdf1',
            point=90500.00
        )

        User.objects.create(
            id=2,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            nickname='정현',
            email='wjdgus@gmail.com',
            social_id=2,
            profile_image='asdfasdf2',
            point=200000.00
        )

        User.objects.create(
            id=3,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            nickname='경서',
            email='riudtj@gmail.com',
            social_id=3,
            profile_image='asdfasdf3',
            point=300000.00
        )

        PlaceStatus.objects.create(
            id=1,
            status=False
        )

        PlaceStatus.objects.create(
            id=2,
            status=True
        )

        Host.objects.create(
            id=1,
            created_at='2022-14-15',
            updated_at='2022-14-15',
            bank='루비',
            account='1111-1111-1112',
            introduction='안녕',
            user_id=2
        )

        Host.objects.create(
            id=2,
            created_at='2022-14-15',
            updated_at='2022-14-15',
            bank='',
            account='1111-1111-1111',
            introduction='안녕',
            user_id=1
        )

        Place.objects.create(
            id=1,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='로컨 에너테인먼트의 모든것',
            subtitle='집에서 만끽하는 편안함',
            price=25000.00,
            running_time=2,
            running_date='2022-04-01',
            location='포항',
            preparation='닌텐도 스위치',
            max_visitor=10,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/andrew-varnum-uNKyYp616wo-unsplash.jpg',
            close_date='2022-03-25',
            host_id=1,
            status_id=1
        )

        Place.objects.create(
            id=2,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='포항의 밥 누나 경서님과 쉽게 그리는 미술',
            subtitle='야! 너두 미술 할수있어',
            price=100000.00,
            running_time=3,
            running_date='2022-05-21',
            location='제주도',
            preparation='물감,스케치북, 도화지',
            max_visitor=1,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/ankhesenamun-KitGM-GDgOI-unsplash.jpg',
            close_date='2022-05-14',
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=3,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='JihunPark과 함께하는 스텐드 코미디',
            subtitle='여러분의 1시간 재미 보장합니다',
            price=3000.00,
            running_time=1,
            running_date='2022-07-21',
            location='신사',
            preparation='물감,스케치북, 도화지',
            max_visitor=500,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/artem-bryzgalov-RdZTQhQuQdE-unsplash.jpg',
            close_date='2022-07-14',
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=4,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='혹시 고민 많은 당신 대화 할까요?',
            subtitle='당신의 눈동자에 cheers~',
            price=45000.00,
            running_time=3,
            running_date='2022-10-08',
            location='강남역',
            preparation='취하지 않을 정신',
            max_visitor=1,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/carson-masterson-yuxr5ohFB-g-unsplash.jpg',
            close_date='2022-10-01',
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=5,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='혹맥주에 매력에 빠져볼까요?',
            subtitle='힘든 시기 같이 맥주 먹으면 서 이야기 할까요?',
            price=3500.00,
            running_time=1,
            running_date='2022-05-22',
            location='익산',
            preparation='빠른 맥주마시기',
            max_visitor=100,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/christin-hume-08tX2fsuSLg-unsplash.jpg',
            close_date='2022-05-15',
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=6,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='이길거란 희망...',
            subtitle='혼자 놀기 심심하셨죠? 같이 놀아요',
            price=10000.00,
            running_time=2,
            running_date='2022-12-21',
            location='선릉역 4번출구',
            preparation='몸만 오시면 됩니다^^',
            max_visitor=5,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/dayne-topkin-xTmqoidRoKQ-unsplash.jpg',
            close_date='2022-12-14',
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=7,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='화려한 조명이 나를 감싸네',
            subtitle='센빠이 광수와 함께하는 늦은오후 티타임',
            price=20000.00,
            running_time=1,
            running_date='2022-06-21',
            location='강남역 11번출구',
            preparation='센커피, 노트북, 핸드폰',
            max_visitor=6,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/dimitris-chapsoulas-MI4QbY979hM-unsplash.jpg',
            close_date='2022-06-14',
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=9,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='야 너도 노래할수 있어',
            subtitle='4집가수 산님 과 함께하는 즐거운 보컬 트레이닝',
            price=70000.00,
            running_time=2,
            running_date='2022-07-31',
            location='관악구 봉천동',
            preparation='목소리',
            max_visitor=2,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/gordon-cowie-3ecKARVRbis-unsplash.jpg',
            close_date='2022-07-24',
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=10,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='오싹한 방탈출',
            subtitle='과연 한시간안에 나갈수있을거 같아?',
            price=19000.00,
            running_time=1,
            running_date='2022-03-10',
            location='강남역 10번출구',
            preparation='smart한 두뇌, 도망가지않을 담력',
            max_visitor=2,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/gryffyn-m-K07OmIlzo90-unsplash.jpg',
            close_date='2022-03-03',
            host_id=1,
            status_id=1
        )

        Reservation.objects.create(
            id=1,
            created_at='2020-04-15',
            updated_at='2020-04-15',
            place_id=1,
            user_id=1
        )

        Reservation.objects.create(
            id=2,
            created_at='2020-04-15',
            updated_at='2020-04-15',
            place_id=7,
            user_id=1
        )

        Reservation.objects.create(
            id=4,
            created_at='2020-04-15',
            updated_at='2020-04-15',
            place_id=9,
            user_id=1
        )

        Reservation.objects.create(
            id=10,
            created_at='2020-04-15',
            updated_at='2020-04-15',
            place_id=3,
            user_id=1
        )

        Reservation.objects.create(
            id=12,
            created_at='2020-04-15',
            updated_at='2020-04-15',
            place_id=5,
            user_id=1
        )

        Reservation.objects.create(
            id=17,
            created_at='2020-04-15',
            updated_at='2020-04-15',
            place_id=2,
            user_id=2
        )

        Reservation.objects.create(
            id=22,
            created_at='2020-04-15',
            updated_at='2020-04-15',
            place_id=2,
            user_id=3
        )

    def tearDown(self):
        User.objects.all().delete()
        PlaceStatus.objects.all().delete()
        Host.objects.all().delete()
        Place.objects.all().delete()
        Reservation.objects.all().delete()

    def test_success_new_place_place_list_with_get_method(self, status='new_place', participant='', sort=''):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        place_list = Place.objects.filter(q)

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_finished_place_place_list_with_get_method(self, status='finished_place', participant='', sort=''):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "finished_place":
            q &= Q(running_date__lte=datetime.now())

        place_list = Place.objects.filter(q)

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_every_place_place_list_with_get_method(self, status      = 'new_place',
                                                                                participant = 'every_place',
                                                                                sort        = ''):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "every_place":
            pass

        place_list = Place.objects.filter(q)

        self.assertEqual(response.json(), {
                                'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_full_visitor_place_list_with_get_method(self, status      = 'new_place',
                                                                                 participant = 'full_visitor',
                                                                                 sort        = ''):
        client   = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "full_visitor":
            place_list = Place.objects.annotate(count=Count("reservation__id")) \
                                      .filter(q, count__gte=F('max_visitor'))

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_less_visitor_place_list_with_get_method(self, status      = 'new_place',
                                                                                 participant = 'less_visitor',
                                                                                 sort        = ''):
        client   = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "less_visitor":
            place_list = Place.objects.annotate(count=Count("reservation__id")) \
                                      .filter(q, count__lt=F('max_visitor'))

        User.objects.create(
            id=2,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            nickname='정현',
            email='wjdgus@gmail.com',
            social_id=2,
            profile_image='http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_640x640.jpg',
            point=200000.00
        )

        User.objects.create(
            id=3,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            nickname='경서',
            email='riudtj@gmail.com',
            social_id=3,
            profile_image='http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_640x640.jpg',
            point=300000.00
        )

        PlaceStatus.objects.create(
            id=1,
            status=False
        )

        PlaceStatus.objects.create(
            id=2,
            status=True
        )

        Host.objects.create(
            id=1,
            created_at='2022-14-15',
            updated_at='2022-14-15',
            bank='루비',
            account='1111-1111-1112',
            introduction='안녕',
            user_id=2
        )

        Host.objects.create(
            id=2,
            created_at='2022-14-15',
            updated_at='2022-14-15',
            bank='다이아',
            account='1111-1111-1111',
            introduction='안녕',
            user_id=1
        )

        Place.objects.create(
            id=3,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='JihunPark과 함께하는 스텐드 코미디',
            subtitle='여러분의 1시간 재미 보장합니다',
            price=3000.00,
            running_time=1,
            running_date='2022-07-21',
            location='신사',
            preparation='물감,스케치북, 도화지',
            max_visitor=500,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/artem-bryzgalov-RdZTQhQuQdE-unsplash.jpg',
            close_date='2022-07-14',
            latitude=37.5213660000,
            longitude=127.0216230000,
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=5,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='혹맥주에 매력에 빠져볼까요?',
            subtitle='힘든 시기 같이 맥주 먹으면 서 이야기 할까요?',
            price=3500.00,
            running_time=1,
            running_date='2022-05-22',
            location='익산',
            preparation='빠른 맥주마시기',
            max_visitor=100,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/christin-hume-08tX2fsuSLg-unsplash.jpg',
            close_date='2022-05-15',
            latitude=35.9594950000,
            longitude=126.9751500000,
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=6,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='이길거란 희망...',
            subtitle='혼자 놀기 심심하셨죠? 같이 놀아요',
            price=10000.00,
            running_time=2,
            running_date='2022-12-21',
            location='선릉역 4번출구',
            preparation='몸만 오시면 됩니다^^',
            max_visitor=5,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/dayne-topkin-xTmqoidRoKQ-unsplash.jpg',
            close_date='2022-12-14',
            latitude=37.5056900000,
            longitude=127.0492960000,
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=18,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='인생 선배 창환님과 함께하는 티타임!!!',
            subtitle='젊은 당신!! 인생 선배의 조언과 함께 미래를 설계해보는 건 어떨까요?',
            price=5000.00,
            running_time=2,
            running_date='2022-01-20',
            location='장승배기역',
            preparation='경청하는 자세',
            max_visitor=10,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/nathan-dumlao-71u2fOofI-U-unsplash.jpg',
            close_date='2022-01-13',
            latitude=37.5050560000,
            longitude=126.9386210000,
            host_id=1,
            status_id=1
        )

        Place.objects.create(
            id=19,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='응애~ 아이들과 함께 키즈 파티!!',
            subtitle='아이와 함께 꾸며놓은 집에 와서 같이 즐거운 시간 보내실 분들 모집합니다!!',
            price=20000.00,
            running_time=4,
            running_date='2022-05-05',
            location='선릉역',
            preparation='간단한 간식거리',
            max_visitor=11,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/nathan-dumlao-H4hXvcedBtM-unsplash.jpg',
            close_date='2022-04-28',
            latitude=37.5086820000,
            longitude=127.0485210000,
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=21,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='박경서를 이겨라 하나! 둘! 셋!',
            subtitle='엠티 추억을 다시 느끼고 싶으신 분들 게임대장 박경서와 함께 추억의 엠티 게임을 해봅시다!',
            price=40000.00,
            running_time=4,
            running_date='2022-04-25',
            location='양평구',
            preparation='편안한 옷차림',
            max_visitor=13,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/point3d-commercial-imaging-ltd-0H-aJ06IZw4-unsplash.jpg',
            close_date='2022-04-18',
            latitude=37.5343310000,
            longitude=126.9008370000,
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=28,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='화분과 함께하는 힐링',
            subtitle='집에 화분이 없는분들은 여기로~',
            price=30000.00,
            running_time=1,
            running_date='2022-04-30',
            location='인천',
            preparation='힐링할준비^^',
            max_visitor=20,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/sidekix-media-1vMz2_MclrM-unsplash.jpg',
            close_date='2022-04-23',
            latitude=37.4692220000,
            longitude=126.5950680000,
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=30,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='식목원이 집안에 있다!?',
            subtitle='식물에 둘러쌓이고 싶은 분 어서 오세요',
            price=40000.00,
            running_time=2,
            running_date='2022-05-02',
            location='경주',
            preparation='카메라',
            max_visitor=5,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/spacejoy-YI2YkyaREHk-unsplash.jpg',
            close_date='2022-04-25',
            latitude=35.8472370000,
            longitude=129.1926070000,
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=31,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='제빵왕 김탁구',
            subtitle='요즘 빵 너무 비싸니까 직접 만들어 먹어요!',
            price=70000.00,
            running_time=4,
            running_date='2022-08-07',
            location='삼성역 5번출구',
            preparation='빵을 좋아하는 마음',
            max_visitor=6,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/tabitha-turner-Ns2aJ5OXKds-unsplash.jpg',
            close_date='2022-07-31',
            latitude=37.5124710000,
            longitude=127.0625590000,
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=32,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='반죽으로 신나게 펑펑',
            subtitle='반죽을 만든다음에 다양한 요리로~',
            price=50000.00,
            running_time=2,
            running_date='2022-03-17',
            location='성북구 동선동',
            preparation='반죽으로 놀고싶은분',
            max_visitor=7,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/theme-photos-Hx7xdwhj2AY-unsplash.jpg',
            close_date='2022-03-10',
            latitude=37.5930300000,
            longitude=127.0163650000,
            host_id=1,
            status_id=1
        )

        Place.objects.create(
            id=33,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='책 읽으면서 뒹굴뒹굴',
            subtitle='이 시간만큼은 아무것도 생각말고 책만 읽기',
            price=30000.00,
            running_time=3,
            running_date='2022-05-19',
            location='상봉역 3번출구',
            preparation='책 오래읽을 마음',
            max_visitor=8,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/toa-heftiba-TGPQumzFRMo-unsplash.jpg',
            close_date='2022-05-12',
            latitude=37.6074500000,
            longitude=127.0917780000,
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=34,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='해병대 캠프',
            subtitle='해병대분들 컴온 ^^',
            price=15000.00,
            running_time=8,
            running_date='2022-07-31',
            location='전주시 완산구',
            preparation='소금, 십자가',
            max_visitor=9,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/yener-ozturk-_u3rMKylNdQ-unsplash.jpg',
            close_date='2022-07-24',
            latitude=35.8210010000,
            longitude=127.1414760000,
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=9,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='야 너도 노래할수 있어',
            subtitle='4집가수 산님 과 함께하는 즐거운 보컬 트레이닝',
            price=70000.00,
            running_time=2,
            running_date='2022-07-31',
            location='관악구 봉천동',
            preparation='목소리',
            max_visitor=2,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/gordon-cowie-3ecKARVRbis-unsplash.jpg',
            close_date='2022-07-24',
            latitude=37.4765540000,
            longitude=126.9601600000,
            host_id=2,
            status_id=2
        )

        Place.objects.create(
            id=10,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='오싹한 방탈출',
            subtitle='과연 한시간안에 나갈수있을거 같아?',
            price=19000.00,
            running_time=1,
            running_date='2022-03-10',
            location='강남역 10번출구',
            preparation='smart한 두뇌, 도망가지않을 담력',
            max_visitor=2,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/gryffyn-m-K07OmIlzo90-unsplash.jpg',
            close_date='2022-03-03',
            latitude=37.4990410000,
            longitude=127.0266110000,
            host_id=1,
            status_id=1
        )

    def tearDown(self):
        User.objects.all().delete()
        PlaceStatus.objects.all().delete()
        Host.objects.all().delete()
        Place.objects.all().delete()

    def test_success_main_place_list_with_get_method(self):
        client = Client()
        response = client.get(f'/places/main')

        place_list_1 = Place.objects.filter().order_by('-created_at')[0:4]
        place_list_2 = Place.objects.filter().order_by('price')[0:4]
        place_list_3 = Place.objects.filter(running_date__gt=datetime.now()).order_by('running_date')[0:4]

        self.assertEqual(response.json(), {
                                    'create_time' : [{
                                        'id'           : place.id,
                                        'img_url'      : place.image_url,
                                        'title'        : place.title,
                                        'subtitle'     : place.subtitle,
                                        'location'     : place.location,
                                        'running_date' : place.running_date.strftime("%Y-%m-%d"),
                                        'price'        : str(place.price)
                                    } for place in place_list_1],

                                    'low_price' : [{
                                        'id'           : place.id,
                                        'img_url'      : place.image_url,
                                        'title'        : place.title,
                                        'subtitle'     : place.subtitle,
                                        'location'     : place.location,
                                        'running_date' : place.running_date.strftime("%Y-%m-%d"),
                                        'price'        : str(place.price)
                                    } for place in place_list_2],

                                    'running_date' : [{
                                        'id'           : place.id,
                                        'img_url'      : place.image_url,
                                        'title'        : place.title,
                                        'subtitle'     : place.subtitle,
                                        'location'     : place.location,
                                        'running_date' : place.running_date.strftime("%Y-%m-%d"),
                                        'price'        : str(place.price)
                                    } for place in place_list_3]
                            }
                        )

        self.assertEqual(response.status_code, 200)


class PlaceReviewListTest(TestCase):
    def setUp(self):
        User.objects.create(
            id=1,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            nickname='이산',
            email='dltks@gmail.com',
            social_id=1,
            profile_image='asdfasdf1',
            point=100000.00
        )

        PlaceStatus.objects.create(
            id=1,
            status=False
        )

        Host.objects.create(
            id=1,
            created_at='2022-14-15',
            updated_at='2022-14-15',
            bank='다이아',
            account='1111-1111-1111',
            introduction='안녕',
            user_id=1
        )

        Place.objects.create(
            id=1,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='로컨 에너테인먼트의 모든것',
            subtitle='집에서 만끽하는 편안함',
            price=25000.00,
            running_time=2,
            running_date='2022-04-01',
            location='포항',
            preparation='닌텐도 스위치',
            max_visitor=10,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/andrew-varnum-uNKyYp616wo-unsplash.jpg',
            close_date='2022-03-25',
            latitude=1,
            longitude=1,
            host_id=1,
            status_id=1
        )

        Review.objects.create(
            id=1,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            content='모름',
            place_id=1,
            user_id=1
        )

    def tearDown(self):
        User.objects.all().delete()
        PlaceStatus.objects.all().delete()
        Host.objects.all().delete()
        Place.objects.all().delete()
        Review.objects.all().delete()

    def test_success_place_review_list_with_get_method(self, place_id=1):
        client   = Client()
        response = client.get(f'/places/{place_id}/review')

        place    = Place.objects.get(id=place_id)

        self.assertEqual(response.json(), {
                'result': [{
                        'nickname'     : review.user.nickname,
                        'content'      : review.content,
                        'running_date' : place.running_date.strftime("%Y-%m-%d"),
                    } for review in Review.objects.filter(place_id=place_id)]
                }
            )
        self.assertEqual(response.status_code, 200)

    def test_fail_place_does_not_exist_error_with_get_method(self, place_id=35):
        client   = Client()
        response = client.get(f'/places/{place_id}/review')

        self.assertEqual(response.json(), {
                    'message': 'Place does not exit'
                }
            )

        self.assertEqual(response.status_code, 404)


class PlaceHostInformationTest(TestCase):
    def setUp(self):
        User.objects.create(
            id=1,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            nickname='이산',
            email='dltks@gmail.com',
            social_id=1,
            profile_image='asdfasdf1',
            point=100000.00
        )

        PlaceStatus.objects.create(
            id=1,
            status=False
        )

        Host.objects.create(
            id=1,
            created_at='2022-14-15',
            updated_at='2022-14-15',
            bank='다이아',
            account='1111-1111-1111',
            introduction='안녕',
            user_id=1
        )

        Place.objects.create(
            id=1,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='로컨 에너테인먼트의 모든것',
            subtitle='집에서 만끽하는 편안함',
            price=25000.00,
            running_time=2,
            running_date='2022-04-01',
            location='포항',
            preparation='닌텐도 스위치',
            max_visitor=10,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/andrew-varnum-uNKyYp616wo-unsplash.jpg',
            close_date='2022-03-25',
            latitude=1,
            longitude=1,
            host_id=1,
            status_id=1
        )

    def tearDown(self):
        User.objects.all().delete()
        PlaceStatus.objects.all().delete()
        Host.objects.all().delete()
        Place.objects.all().delete()

    def test_success_place_Host_information_with_get_method(self, place_id=1):
        client   = Client()
        response = client.get(f'/places/{place_id}/hostinformation')

        place = Place.objects.select_related('host').get(id=place_id)

        self.assertEqual(response.json(), {
                        'result': {
                            'host_nickname'      : place.host.user.nickname,
                            'host_profile_image' : place.host.user.profile_image,
                            'host_introduction'  : place.host.introduction
                             }
                        }
                )
        self.assertEqual(response.status_code, 200)


class PlaceSearchTest(TestCase):
    def setUp(self):
        User.objects.create(
            id=1,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            nickname='이산',
            email='dltks@gmail.com',
            social_id=1,
            profile_image='asdfasdf1',
            point=90500.00
        )

        PlaceStatus.objects.create(
            id=2,
            status=True
        )

        Host.objects.create(
            id=2,
            created_at='2022-14-15',
            updated_at='2022-14-15',
            bank='',
            account='1111-1111-1111',
            introduction='안녕',
            user_id=1
        )

        Place.objects.create(
            id=3,
            created_at='2022-04-15',
            updated_at='2022-04-15',
            title='JihunPark과 함께하는 스텐드 코미디',
            subtitle='여러분의 1시간 재미 보장합니다',
            price=3000.00,
            running_time=1,
            running_date='2022-07-21',
            location='신사',
            preparation='물감,스케치북, 도화지',
            max_visitor=500,
            image_url='https://wecode-withme.s3.ap-northeast-2.amazonaws.com/images/artem-bryzgalov-RdZTQhQuQdE-unsplash.jpg',
            close_date='2022-07-14',
            latitude=1,
            longitude=1,
            host_id=2,
            status_id=2
            )

    def tearDown(self):
        User.objects.all().delete()
        PlaceStatus.objects.all().delete()
        Host.objects.all().delete()
        Place.objects.all().delete()

    def test_success_places_search_with_get_method(self, k='로컬'):
        client = Client()
        response = client.get(f'/places/search?k={k}')

        q = Q()

        if k:
            q &= Q(title__icontains=k)

        places = Place.objects.filter(q)

        self.assertEqual(response.json(), {
                            'result' : [{
                                'id': place.id,
                                'img_url': place.image_url,
                                'title': place.title,
                                'subtitle': place.subtitle,
                                'location': place.location,
                                'price': place.price
                            }for place in places]
                        }
                    )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_deadline_place_list_with_get_method(self, status      = 'new_place',
                                                                             participant = '',
                                                                             sort        = 'deadline'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        place_list = Place.objects.filter(q)

        if sort == "deadline":
            place_list = place_list.order_by('running_date')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_permitted_place_list_with_get_method(self, status      = 'new_place',
                                                                              participant = '',
                                                                              sort        = 'permitted'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        place_list = Place.objects.filter(q)

        if sort == "permitted":
            place_list = place_list.order_by('-created_at')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_low_price_place_list_with_get_method(self, status      = 'new_place',
                                                                              participant = '',
                                                                              sort        = 'low_price'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        place_list = Place.objects.filter(q)

        if sort == "low_price":
            place_list = place_list.order_by('price')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_high_price_place_list_with_get_method(self, status      = 'new_place',
                                                                               participant = '',
                                                                               sort        = 'high_price'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        place_list = Place.objects.filter(q)

        if sort == "high_price":
            place_list = place_list.order_by('-price')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_every_place_and_deadline_place_list_with_get_method(self, status = 'new_place',
                                                                                       participant  = 'every_place',
                                                                                       sort         = 'deadline'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "every_place":
            pass

        place_list = Place.objects.filter(q)

        if sort == "deadline":
            place_list = place_list.order_by('running_date')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_every_place_and_permitted_place_list_with_get_method(self, status = 'new_place',
                                                                                        participant  = 'every_place',
                                                                                        sort         ='permitted'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "every_place":
            pass

        place_list = Place.objects.filter(q)

        if sort == "permitted":
            place_list = place_list.order_by('-created_at')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_every_place_and_low_price_place_list_with_get_method(self, status = 'new_place',
                                                                                        participant  = 'every_place',
                                                                                        sort         ='low_price'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "every_place":
            pass

        place_list = Place.objects.filter(q)

        if sort == "low_price":
            place_list = place_list.order_by('price')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_every_place_and_high_price_place_list_with_get_method(self, status = 'new_place',
                                                                                         participant  = 'every_place',
                                                                                         sort         = 'high_price'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "every_place":
            pass

        place_list = Place.objects.filter(q)

        if sort == "high_price":
            place_list = place_list.order_by('-price')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_full_visitor_and_deadline_place_list_with_get_method(self, status = 'new_place',
                                                                                        participant  = 'full_visitor',
                                                                                        sort         = 'deadline'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "full_visitor":
            place_list = Place.objects.annotate(count=Count("reservation__id")) \
                .filter(q, count__gte=F('max_visitor'))

        if sort == "deadline":
            place_list = place_list.order_by('running_date')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_full_visitor_and_permitted_place_list_with_get_method(self, status = 'new_place',
                                                                                         participant  = 'full_visitor',
                                                                                         sort         = 'permitted'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "full_visitor":
            place_list = Place.objects.annotate(count=Count("reservation__id")) \
                .filter(q, count__gte=F('max_visitor'))

        if sort == "permitted":
            place_list = place_list.order_by('-created_at')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_full_visitor_and_low_price_place_list_with_get_method(self, status = 'new_place',
                                                                                         participant  = 'full_visitor',
                                                                                         sort         = 'low_price'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "full_visitor":
            place_list = Place.objects.annotate(count=Count("reservation__id")) \
                .filter(q, count__gte=F('max_visitor'))

        if sort == "low_price":
            place_list = place_list.order_by('price')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_full_visitor_and_high_price_place_list_with_get_method(self, status = 'new_place',
                                                                                         participant   = 'full_visitor',
                                                                                         sort          = 'high_price'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "full_visitor":
            place_list = Place.objects.annotate(count=Count("reservation__id")) \
                .filter(q, count__gte=F('max_visitor'))

        if sort == "high_price":
            place_list = place_list.order_by('-price')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_less_visitor_and_deadline_place_list_with_get_method(self, status = 'new_place',
                                                                                        participant  = 'less_visitor',
                                                                                        sort         = 'deadline'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "less_visitor":
            place_list = Place.objects.annotate(count=Count("reservation__id")) \
                .filter(q, count__lt=F('max_visitor'))

        if sort == "deadline":
            place_list = place_list.order_by('running_date')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_less_visitor_and_permitted_place_list_with_get_method(self, status = 'new_place',
                                                                                        participant   = 'less_visitor',
                                                                                        sort          = 'permitted'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "less_visitor":
            place_list = Place.objects.annotate(count=Count("reservation__id")) \
                .filter(q, count__lt=F('max_visitor'))

        if sort == "permitted":
            place_list = place_list.order_by('-created_at')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_less_visitor_and_low_price_place_list_with_get_method(self, status = 'new_place',
                                                                                        participant   = 'less_visitor',
                                                                                        sort          = 'low_price'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "less_visitor":
            place_list = Place.objects.annotate(count=Count("reservation__id")) \
                .filter(q, count__lt=F('max_visitor'))

        if sort == "low_price":
            place_list = place_list.order_by('price')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_new_place_and_less_visitor_and_low_high_place_list_with_get_method(self, status = 'new_place',
                                                                                        participant  = 'less_visitor',
                                                                                        sort         = 'high_price'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "less_visitor":
            place_list = Place.objects.annotate(count=Count("reservation__id")) \
                .filter(q, count__lt=F('max_visitor'))

        if sort == "high_price":
            place_list = place_list.order_by('-price')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )

        self.assertEqual(response.status_code, 200)

    def test_success_deadline_place_list_with_get_method(self, status = '', participant = '',
                                                               sort = 'deadline'):
        client = Client()
        response = client.get(f'/places/placelist?status={status}&participant={participant}&sort={sort}')

        q = Q()

        if status == "new_place":
            q &= Q(running_date__gt=datetime.now())

        if participant == "every_place":
            pass

        place_list = Place.objects.filter(q)

        if sort == "deadline":
            place_list = place_list.order_by('running_date')

        self.assertEqual(response.json(), {
                                    'result': [{
                                    'id'          : place.id,
                                    'img_url'     : place.image_url,
                                    'max_visitor' : place.max_visitor,
                                    'title'       : place.title,
                                    'subtitle'    : place.subtitle,
                                    'location'    : place.location,
                                    'running_date': place.running_date.strftime("%Y-%m-%d"),
                                    'price'       : str(place.price)
                                } for place in place_list]
                            }
                        )