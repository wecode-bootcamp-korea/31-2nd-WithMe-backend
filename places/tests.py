from django.test import TestCase, Client

from places.models import Place, PlaceStatus, Review
from users.models import User, Host


class PlaceDetailTest(TestCase):
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

    def test_success_place_detail_page_with_get_method(self, place_id=1):
        client   = Client()
        response = client.get(f'/places/detail/{place_id}')

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
                    'host': {
                        'host_nickname'      : User.objects.get(id=place.host_id).nickname,
                        'host_profile_image' : User.objects.get(id=place.host_id).profile_image,
                        'host_introduction'  : place.host.introduction
                        },
                    'review_list': [{
                        'nickname'     : review.user.nickname,
                        'content'      : review.content,
                        'running_date' : place.running_date.strftime("%Y-%m-%d"),
                    } for review in Review.objects.filter(place_id=place_id)]
                    }
                }
            )
        self.assertEqual(response.status_code, 200)

    def test_fail_place_does_not_exist_error_with_get_method(self, place_id=35):
        client   = Client()
        response = client.get(f'/places/detail/{place_id}')

        self.assertEqual(response.json(), {
                    'result': 'Place does not exit'
                }
            )

        self.assertEqual(response.status_code, 404)