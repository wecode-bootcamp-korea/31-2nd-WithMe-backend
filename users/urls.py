from django.urls import path

from users.views import KakaoLoginView,MypageView,PointView,ReviewView

urlpatterns = [
    path('/signin',KakaoLoginView.as_view()),
    path('/mypage',MypageView.as_view()),
    path('/mypage/point',PointView.as_view()),
    path('/mypage/review',ReviewView.as_view()),
]
