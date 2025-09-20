from django.urls import path

from adminunits.views import (
    UnitListView, UnitListOnMapView, UnitView, DataView, UnitNameView, UnitParentView,
)


urlpatterns = [
    path('', UnitView.as_view(), name='unit_create'),
    path('<int:unit_id>/', UnitView.as_view(), name='unit_edit_or_get'),

    path('<int:unit_id>/names/', UnitNameView.as_view(), name='unit_names_get'),
    path('<int:unit_id>/name/<int:name_id>/', UnitNameView.as_view(), name='unit_name_edit'),
    path('<int:unit_id>/name/', UnitNameView.as_view(), name='unit_name_create'),

    path('<int:unit_id>/parents/', UnitParentView.as_view(), name='unit_parents_get'),
    path('<int:unit_id>/parent/<int:including_id>/', UnitParentView.as_view(), name='unit_parent_edit'),

    path('list/', UnitListView.as_view(), name='units_list'),
    path('list_for_map/', UnitListOnMapView.as_view(), name='units_list_for_map'),
    path('data/', DataView.as_view(), name='data'),
]
