from django.core.management.base import BaseCommand, CommandError

from adminunits.models import UNIT_TYPES, Unit, UnitName
from adminunits.utils import add_date_args_to_parser, populate_kwargs_by_date, populate_kwargs_by_part_date


class Command(BaseCommand):
    help = 'Manipulate your historical administrative units'

    def add_arguments(self, parser):
        parser.add_argument('name', nargs=1, type=str)
        add_date_args_to_parser(parser)

    def handle(self, *args, **options):
        self.stdout.write('Варианты типов АТЕ:')
        for unit_type_id, unit_type_name in UNIT_TYPES:
            self.stdout.write(f'  {unit_type_id} - {unit_type_name}')

        self.stdout.write('Укажите номер выбранного типа АТЕ:')
        unit_type = int(input())
        name_kwargs = {}
        populate_kwargs_by_date(name_kwargs, 'start', options['sdate'])
        populate_kwargs_by_date(name_kwargs, 'end', options['edate'])
        populate_kwargs_by_part_date(name_kwargs, options)

        unit = Unit(type=unit_type)
        unit.save()
        unit_name = UnitName(unit=unit, name=options['name'][0], **name_kwargs)
        unit_name.save()

        self.stdout.write(f'ID созданной АТЕ: {unit.id}-{unit_name.id}')
