from django.contrib.gis.geos import Polygon
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from adminunits.models import Including, UnitName, UNIT_TYPE_COUNTRY, UNIT_TYPE_SETTLEMENT

DEFAULT_YEAR = '1708'


class UnitListView(APIView):
    def get(self, request):
        year = request.GET.get('year', DEFAULT_YEAR)
        parent_unit_id = request.GET.get('parent')
        data = []
        kwargs = {}
        if parent_unit_id:
            if year:
                year = int(year)
                kwargs['child__names__start_year__lte'] = year
                kwargs['child__names__end_year__gt'] = year

            includings = (
                Including.objects.filter(parent_id=int(parent_unit_id), **kwargs)
                .values('child__id', 'child__names__name', 'child__names__start_year', 'child__names__end_year')
                .order_by('child__names__name')
            )
            for unit_dict in includings:
                data.append({
                    'id': unit_dict['child__id'],
                    'name': unit_dict['child__names__name'],
                    'start_year': unit_dict['child__names__start_year'],
                    'end_year': unit_dict['child__names__end_year'],
                })
        else:
            if year:
                year = int(year)
                kwargs['start_year__lte'] = year
                kwargs['end_year__gt'] = year

            unit_names = UnitName.objects.filter(unit__type=UNIT_TYPE_COUNTRY, **kwargs).order_by('name')
            for unit_name in unit_names:
                data.append({
                    'id': unit_name.unit.pk,
                    'name': unit_name.name,
                    'start_year': unit_name.start_year,
                    'end_year': unit_name.end_year,
                })

        return Response(status=status.HTTP_200_OK, data=data)


class UnitListOnMapView(APIView):
    def get(self, request):
        year = request.GET.get('year', DEFAULT_YEAR)
        polygon_points = [float(value) for value in request.GET['polygon'].split(',')]
        polygon = Polygon.from_bbox(polygon_points)
        data = []
        kwargs = {}
        args = []
        if year:
            year = int(year)
            args.append(Q(unit__start_year__lte=year) | Q(unit__start_year__isnull=True))
            args.append(Q(unit__end_year__gt=year) | Q(unit__end_year__isnull=True))

        unit_names = (
            UnitName.objects.filter(*args, unit__type=UNIT_TYPE_SETTLEMENT, **kwargs)
            .filter(unit__point__isnull=False, unit__point__contained=polygon)
            .values('unit__pk', 'name', 'unit__point', 'unit__start_year', 'unit__end_year')
        )
        for unit_name in unit_names:
            data.append({
                'id': unit_name['unit__pk'],
                'name': unit_name['name'],
                'point': list(unit_name['unit__point']),
                's': unit_name['unit__start_year'],
                'e': unit_name['unit__end_year'],
            })

        return Response(status=status.HTTP_200_OK, data=data)
