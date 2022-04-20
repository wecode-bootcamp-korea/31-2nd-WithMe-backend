from django.urls import path

from users.views import KakaoLoginView, UserInfomation, ReviewView, ReservationView

urlpatterns = [
    path('/signin',KakaoLoginView.as_view()),
    path('/userinfo',UserInfomation.as_view()),
    path('/reservation',ReservationView.as_view()),
    path('/review',ReviewView.as_view()),
]
