from django.urls import path

from adminunits.views import UnitListView

urlpatterns = [
    path('list/', UnitListView.as_view(), name='units_list'),
]
