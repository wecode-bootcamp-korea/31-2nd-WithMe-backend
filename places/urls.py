from django.urls import path
from places.views import PlaceInformationView


urlpatterns = [
    path('/placeinformation/<int:place_id>', PlaceInformationView.as_view())
 ]
