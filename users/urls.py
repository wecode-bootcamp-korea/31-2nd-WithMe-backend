from django.urls import path

from users.views import KakaoLoginView,PointChargeView,HostMainView, HostRegisterView, PlaceRegisterView

urlpatterns = [
    path('/signin',KakaoLoginView.as_view()),
    path('/point',PointChargeView.as_view()),
    path('/hosts', HostMainView.as_view()),
    path('/hosts/hostregist', HostRegisterView.as_view()),
    path('/hosts/hostregist/<int:host_id>', HostRegisterView.as_view()),
    path('/hosts/placeregist', PlaceRegisterView.as_view()),
]
