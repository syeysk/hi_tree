from django.core.management.base import BaseCommand, CommandError

from adminunits.models import Including
from adminunits.utils import add_date_args_to_parser, populate_kwargs_by_date, populate_kwargs_by_part_date


class Command(BaseCommand):
    help = 'Manipulate your historical administrative units'

    def add_arguments(self, parser):
        parser.add_argument('including-id', nargs='+', type=int)
        parser.add_argument('--child-unit-id', nargs='?', type=int, required=False)
        parser.add_argument('--parent-unit-id', nargs='?', type=int, required=False)
        add_date_args_to_parser(parser)

    def handle(self, *args, **options):
        including_ids = options['including-id']
        child_id = options['child_unit_id']
        parent_id = options['parent_unit_id']

        name_kwargs = {}
        if child_id:
            name_kwargs['child'] = child_id

        if parent_id:
            name_kwargs['parent'] = parent_id

        populate_kwargs_by_date(name_kwargs, 'start', options['sdate'])
        populate_kwargs_by_date(name_kwargs, 'end', options['edate'])
        populate_kwargs_by_part_date(name_kwargs, options)

        if name_kwargs:
            Including.objects.filter(id__in=including_ids).update(**name_kwargs)
            self.stdout.write(self.style.SUCCESS(f'Включение АТЕ успешно изменена'))
