from django.urls import path
from places.views import PlaceInformationView, MainPlaceListView

urlpatterns = [
    path('/placeinformation/<int:place_id>', PlaceInformationView.as_view()),
    path('/main', MainPlaceListView.as_view())
 ]
