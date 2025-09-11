from django.core.management.base import BaseCommand, CommandError

from adminunits.models import UNIT_TYPES, UnitName
from adminunits.utils import add_date_args_to_parser, populate_kwargs_by_date, populate_kwargs_by_part_date


class Command(BaseCommand):
    help = 'Manipulate your historical administrative units'

    def add_arguments(self, parser):
        parser.add_argument('unit-id', nargs=1, type=int)
        parser.add_argument('name', nargs=1, type=str)
        add_date_args_to_parser(parser)

    def handle(self, *args, **options):
        name_kwargs = {}
        populate_kwargs_by_date(name_kwargs, 'start', options['sdate'])
        populate_kwargs_by_date(name_kwargs, 'end', options['edate'])
        populate_kwargs_by_part_date(name_kwargs, options)

        unit_name = UnitName(unit_id=options['unit-id'][0], name=options['name'][0], **name_kwargs)
        unit_name.save()
        self.stdout.write(f'ID созданного имени: {unit_name.id}')
