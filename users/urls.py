from django.urls import path

from users.views import KakaoLoginView,ReviewView

urlpatterns = [
    path('/signin',KakaoLoginView.as_view()),
    path('/mypage/review',ReviewView.as_view()),
]
