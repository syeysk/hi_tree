from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from adminunits.models import Including, UnitName, UNIT_TYPE_COUNTRY


class UnitListView(APIView):
    def get(self, request):
        year = request.GET.get('year')
        parent_unit_id = request.GET.get('parent')
        data = []
        kwargs = {}
        if parent_unit_id:
            if year:
                year = int(year)
                kwargs['child__names__start_year__lte'] = year
                kwargs['child__names__end_year__gte'] = year

            includings = Including.objects.filter(
                parent_id=int(parent_unit_id),
                **kwargs,
            ).values('child__names__id', 'child__names__name', 'child__names__start_year', 'child__names__end_year')
            for unit_dict in includings:
                data.append({
                    'id': unit_dict['child__names__id'],
                    'name': unit_dict['child__names__name'],
                    'start_year': unit_dict['child__names__start_year'],
                    'end_year': unit_dict['child__names__end_year'],
                })
        else:
            if year:
                year = int(year)
                kwargs['start_year__lte'] = year
                kwargs['end_year__gte'] = year

            unit_names = UnitName.objects.filter(unit__type=UNIT_TYPE_COUNTRY, **kwargs)
            for unit_name in unit_names:
                data.append({
                    'id': unit_name.unit.pk,
                    'name': unit_name.name,
                    'start_year': unit_name.start_year,
                    'end_year': unit_name.end_year,
                })

        return Response(status=status.HTTP_200_OK, data=data)
