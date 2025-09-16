from django.urls import path

from adminunits.views import UnitListView, UnitListOnMapView

urlpatterns = [
    path('list/', UnitListView.as_view(), name='units_list'),
    path('list_for_map/', UnitListOnMapView.as_view(), name='units_list_for_map'),
]
