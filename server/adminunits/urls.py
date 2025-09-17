from django.urls import path

from adminunits.views import UnitListView, UnitListOnMapView, UnitView, DataView

urlpatterns = [
    path('', UnitView.as_view(), name='unit_create'),
    path('<int:unit_id>/', UnitView.as_view(), name='unit_edit_or_get'),
    path('list/', UnitListView.as_view(), name='units_list'),
    path('list_for_map/', UnitListOnMapView.as_view(), name='units_list_for_map'),
    path('data/', DataView.as_view(), name='data'),
]
