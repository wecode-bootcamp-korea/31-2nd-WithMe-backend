from django.urls import path

from places.views import PlaceInformationView, MainPlaceListView, PlaceReviewListView, PlaceHostInformationView, \
                                                                  PlaceSearchView, HostResistPlaceList

urlpatterns = [
    path('/placeinformation/<int:place_id>', PlaceInformationView.as_view()),
    path('/main', MainPlaceListView.as_view()),
    path('/<int:place_id>/review', PlaceReviewListView.as_view()),
    path('/placehostinformation', PlaceHostInformationView.as_view()),
    path('/search', PlaceSearchView.as_view()),
    path('/<int:place_id>/hostinformation', PlaceHostInformationView.as_view()),
    path('/hostregstlist', HostResistPlaceList.as_view())
]
