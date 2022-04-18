from django.urls import path

from users.views import KakaoLoginView,PointChargeView

urlpatterns = [
    path('/signin',KakaoLoginView.as_view()),
    path('/point',PointChargeView.as_view()),
]
