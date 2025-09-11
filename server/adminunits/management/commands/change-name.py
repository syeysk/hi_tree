from django.core.management.base import BaseCommand

from adminunits.models import UnitName
from adminunits.utils import add_date_args_to_parser, populate_kwargs_by_date, populate_kwargs_by_part_date


class Command(BaseCommand):
    help = 'Manipulate your historical administrative units'

    def add_arguments(self, parser):
        parser.add_argument('unit-id', nargs=1, type=int)
        parser.add_argument('name-id', nargs=1, type=int)
        parser.add_argument('--name', nargs='?', type=str, required=False)
        parser.add_argument('--unit-id', nargs='?', type=int, required=False)
        add_date_args_to_parser(parser)

    def handle(self, *args, **options):
        unit_id = options['unit-id'][0]
        name_id = options['name-id'][0]
        name = options['name']
        unit_id = options['unit_id']

        name_kwargs = {}
        if name:
            name_kwargs['name'] = name

        if unit_id:
            name_kwargs['unit_id'] = unit_id

        populate_kwargs_by_date(name_kwargs, 'start', options['sdate'])
        populate_kwargs_by_date(name_kwargs, 'end', options['edate'])
        populate_kwargs_by_part_date(name_kwargs, options)

        if name_kwargs:
            UnitName.objects.filter(id=name_id, unit_id=unit_id).update(**name_kwargs)
            self.stdout.write(self.style.SUCCESS(f'Наименование АТЕ успешно изменено'))
