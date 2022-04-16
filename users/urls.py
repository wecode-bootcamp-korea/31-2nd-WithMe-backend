from django.urls import path

from users.views import KakaoLoginView,MypageMainView

urlpatterns = [
    path('/signin',KakaoLoginView.as_view()),
    path('/mypage',MypageMainView.as_view()),
]
