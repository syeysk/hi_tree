from django.contrib.gis.geos import Polygon
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from adminunits.models import Including, Unit, UnitName, UNIT_TYPE_COUNTRY, UNIT_TYPE_SETTLEMENT

DEFAULT_YEAR = '1708'


class UnitListView(APIView):
    def get(self, request):
        year = request.GET.get('year', DEFAULT_YEAR)
        parent_unit_id = request.GET.get('parent')
        data = []
        args = []
        if parent_unit_id:
            if year:
                year = int(year)
                # TODO: искать по дате вхождения, а не именования
                args.append(Q(child__names__start_year__lte=year) | Q(child__names__start_year__isnull=True))
                args.append(Q(child__names__end_year__gt=year) | Q(child__names__end_year__isnull=True))

            includings = (
                Including.objects.filter(*args, parent_id=int(parent_unit_id))
                .values('child__id', 'child__names__name', 'child__names__start_year', 'child__names__end_year', 'child__point')
                .order_by('child__names__name')
            )
            for unit_dict in includings:
                point = unit_dict['child__point']
                data.append({
                    'id': unit_dict['child__id'],
                    'name': unit_dict['child__names__name'],
                    'start_year': unit_dict['child__names__start_year'],
                    'end_year': unit_dict['child__names__end_year'],
                    'point': list(point) if point else None,
                })
        else:
            if year:
                year = int(year)
                args.append(Q(start_year__lte=year) | Q(start_year__isnull=True))
                args.append(Q(end_year__gt=year) | Q(end_year__isnull=True))

            unit_names = UnitName.objects.filter(*args, unit__type=UNIT_TYPE_COUNTRY).order_by('name')
            for unit_name in unit_names:
                point = unit_name.unit.point
                data.append({
                    'id': unit_name.unit.pk,
                    'name': unit_name.name,
                    'start_year': unit_name.start_year,
                    'end_year': unit_name.end_year,
                    'point': list(point) if point else None,
                })

        return Response(status=status.HTTP_200_OK, data=data)


class UnitListOnMapView(APIView):
    def get(self, request):
        year = request.GET.get('year', DEFAULT_YEAR)
        polygon_points = [float(value) for value in request.GET['polygon'].split(',')]
        polygon = Polygon.from_bbox(polygon_points)
        data = []
        args = []
        if year:
            year = int(year)
            args.append(Q(unit__start_year__lte=year) | Q(unit__start_year__isnull=True))
            args.append(Q(unit__end_year__gt=year) | Q(unit__end_year__isnull=True))

        unit_names = (
            UnitName.objects.filter(*args, unit__type=UNIT_TYPE_SETTLEMENT)
            .filter(unit__point__isnull=False, unit__point__contained=polygon)
            .values('unit__pk', 'name', 'unit__point', 'unit__start_year', 'unit__end_year')
        )
        for unit_name in unit_names:
            data.append({
                'id': unit_name['unit__pk'],
                'name': unit_name['name'],
                'point': list(unit_name['unit__point']),
                'start_year': unit_name['unit__start_year'],
                'end_year': unit_name['unit__end_year'],
            })

        return Response(status=status.HTTP_200_OK, data=data)


class UnitView(APIView):
    def put(self, request):
        data = request.data
        data['id'] = 10
        return Response(status=status.HTTP_200_OK, data=data)

    def post(self, request, unit_id):
        data = request.data
        return Response(status=status.HTTP_200_OK, data=data)
    
    def get(self, request, unit_id):
        unit = Unit.objects.filter(id=unit_id).first()
        point = unit.point
        lat, lon = list(point) if point else [None, None]
        parents = []
        unit_names = []
        for unit_name in unit.names.order_by('start_year').all():
            unit_names.append(
                {
                    'name': unit_name.name,
                    'start_year': unit_name.start_year,
                    'start_month': unit_name.start_month,
                    'start_day': unit_name.start_day,
                    'end_year': unit_name.end_year,
                    'end_month': unit_name.end_month,
                    'end_day': unit_name.end_day,
                }
            )
        for including in unit.parent_includings.order_by('start_year').all():
            parents.append(
                {
                    'id': including.parent.id,
                    'including_id': including.id,
                    'name': including.parent.names.first().name,
                    'start_year': including.start_year,
                    'start_month': including.start_month,
                    'start_day': including.start_day,
                    'end_year': including.end_year,
                    'end_month': including.end_month,
                    'end_day': including.end_day,
                }
            )
        data = {
            'lat': lat,
            'lon': lon,
            'start_year': unit.start_year,
            'start_month': unit.start_month,
            'start_day': unit.start_day,
            'end_year': unit.end_year,
            'end_month': unit.end_month,
            'end_day': unit.end_day,
            'type': unit.type,
            'names': unit_names,
            'parents': parents,
        }
        return Response(status=status.HTTP_200_OK, data=data)