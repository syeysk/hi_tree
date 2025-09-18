from django.contrib.gis.geos import Polygon, Point
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from adminunits.models import Including, Unit, UnitName, UNIT_TYPE_COUNTRY, UNIT_TYPE_SETTLEMENT, UNIT_TYPES
from adminunits.serializers import UnitUpdateSerializer

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
        unit = Unit.objects.filter(id=int(data['id'])).first()

        # if 'lat' in data and 'lon' in data:
        #     lat, lon = data.pop('lat'), data.pop('lon')
        #     unit.point = Point(float(lat), float(lon)) if lat and lon else None

        response_data = {}
        serializer = UnitUpdateSerializer(unit, data=request.data)
        serializer.is_valid(raise_exception=True)

        response_data['updated_fields'] = [
            name for name, value in serializer.validated_data.items() if getattr(unit, name) != value
        ]
        serializer.save()

        return Response(status=status.HTTP_200_OK, data=response_data)
    
    def get(self, request, unit_id):
        unit = Unit.objects.filter(id=unit_id).first()
        point = unit.point
        lon, lat = list(point) if point else [None, None]
        parents = []
        unit_names = []
        for unit_name in unit.names.order_by('start_year').all():
            unit_names.append(
                {
                    'name': unit_name.name,
                    'start_date': {
                        'year': unit_name.start_year,
                        'month': unit_name.start_month,
                        'day': unit_name.start_day,
                    },
                    'end_date': {
                        'year': unit_name.end_year,
                        'month': unit_name.end_month,
                        'day': unit_name.end_day,
                    },
                }
            )
        for including in unit.parent_includings.order_by('start_year').all():
            parents.append(
                {
                    'id': including.parent.id,
                    'including_id': including.id,
                    'name': including.parent.names.first().name,
                    'start_date': {
                        'year': including.start_year,
                        'month': including.start_month,
                        'day': including.start_day,
                    },
                    'end_date': {
                        'year': including.end_year,
                        'month': including.end_month,
                        'day': including.end_day,
                    },
                }
            )
        data = {
            'lat': lat,
            'lon': lon,
            'start_date': {
                'year': unit.start_year,
                'month': unit.start_month,
                'day': unit.start_day,
            },
            'end_date': {
                'year': unit.end_year,
                'month': unit.end_month,
                'day': unit.end_day,
            },
            'type': unit.type,
            'names': unit_names,
            'parents': parents,
        }
        return Response(status=status.HTTP_200_OK, data=data)


class DataView(APIView):
    def get(self, request):
        data = {
            'types': dict(UNIT_TYPES),
        }
        return Response(status=status.HTTP_200_OK, data=data)