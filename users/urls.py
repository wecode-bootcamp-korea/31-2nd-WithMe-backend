from django.urls import path

from users.views import KaKaoLoginView

urlpatterns = [
    path('/signin',KaKaoLoginView.as_view()),
]
