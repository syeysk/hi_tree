from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

from adminunits.models import Unit
from adminunits.utils import add_date_args_to_parser, populate_kwargs_by_date, populate_kwargs_by_part_date


class Command(BaseCommand):
    help = 'Manipulate your historical administrative units'

    def add_arguments(self, parser):
        parser.add_argument('unit-id', nargs=1, type=int)
        parser.add_argument('--lat', nargs='?', type=float, required=False)
        parser.add_argument('--lon', nargs='?', type=float, required=False)
        add_date_args_to_parser(parser)

    def handle(self, *args, **options):
        unit_id = options['unit-id'][0]
        lat = options['lat']
        lon = options['lon']
 
        unit_kwargs = {}
        if lat and lon:
            unit_kwargs['point'] = Point(lon, lat)

        populate_kwargs_by_date(unit_kwargs, 'start', options['sdate'])
        populate_kwargs_by_date(unit_kwargs, 'end', options['edate'])
        populate_kwargs_by_part_date(unit_kwargs, options)

        if unit_kwargs:
            Unit.objects.filter(id=unit_id).update(**unit_kwargs)
            self.stdout.write(self.style.SUCCESS(f'АТЕ успешно изменена'))
