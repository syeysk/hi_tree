from django.core.management.base import BaseCommand

from adminunits.models import Including
from adminunits.utils import add_date_args_to_parser, populate_kwargs_by_date, populate_kwargs_by_part_date


class Command(BaseCommand):
    help = 'Manipulate your historical administrative units'

    def add_arguments(self, parser):
        parser.add_argument('parent-unit-id', nargs=1, type=int)
        parser.add_argument('child-unit-ids', nargs='+', type=int)
        add_date_args_to_parser(parser)

    def handle(self, *args, **options):
        unit_id = options['parent-unit-id'][0]
        child_unit_ids = options['child-unit-ids']
        name_kwargs = {}
        populate_kwargs_by_date(name_kwargs, 'start', options['sdate'])
        populate_kwargs_by_date(name_kwargs, 'end', options['edate'])
        populate_kwargs_by_part_date(name_kwargs, options)

        for child_unit_id in child_unit_ids:
            including = Including(child_id=child_unit_id, parent_id=unit_id, **name_kwargs)
            including.save()

        self.stdout.write(f'АТЕ с ID {", ".join([str(i) for i in child_unit_ids])} успешно включены в АТЕ с ID {unit_id}')
