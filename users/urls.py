from django.urls import path

from users.views import KakaoLoginView,UserInfomation

urlpatterns = [
    path('/signin',KakaoLoginView.as_view()),
    path('/userinfo',UserInfomation.as_view())
]
