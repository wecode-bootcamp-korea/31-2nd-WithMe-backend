from django.urls import path
from places.views import PlaceDetailView

urlpatterns = [
    path('/detail/<int:place_id>', PlaceDetailView.as_view())
 ]