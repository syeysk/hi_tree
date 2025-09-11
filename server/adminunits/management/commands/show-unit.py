from os import SEEK_CUR

from django.core.management.base import BaseCommand

from adminunits.models import UnitName, Unit


BOLD = '\x1b[1m'
ITALIC = '\x1b[3m'
RESET = '\x1b[0m'


class Command(BaseCommand):
    help = 'Manipulate your historical administrative units'

    def add_arguments(self, parser):
        parser.add_argument('unit-id', nargs=1, type=int)
        parser.add_argument('--yname', nargs='?', type=int)
        #parser.add_argument('--yinc', nargs='?', type=int)

    def build_date_period(self, obj_with_date):
        period_str = ''
        if obj_with_date.start_date and obj_with_date.end_date:
            period_str = f'{obj_with_date.start_date} - {obj_with_date.end_date}'
        elif obj_with_date.start_date:
            period_str = f'с {obj_with_date.start_date}'
        elif obj_with_date.end_date:
            period_str = f'по {obj_with_date.end_date}'
        
        return period_str.ljust(23)

    def build_name(self, unit_name, including=None):
        dates_str = self.build_date_period(unit_name)
        if dates_str:
            dates_str = f'   {ITALIC}{dates_str}{RESET}'

        unit_name_id_str = str(unit_name.id).rjust(2, '0')
        unit_id_str = str(unit_name.unit.id).rjust(2, '0')
        including_id_str = ''
        if including:
            including_id_str = str(including.id).rjust(2, '0')
            including_id_str = f'.{including_id_str}'

        name_str = unit_name.name.ljust(40)
        return f'  {unit_id_str}.{unit_name_id_str}{including_id_str}  {name_str}{dates_str}'
    
    def print_names(self, unit, including=None):
        kwargs = {}
        self.populate_yname(kwargs)

        for index, unit_name in enumerate(UnitName.objects.filter(unit=unit, **kwargs).order_by('start_year', 'name').all()):
            name_str = self.build_name(unit_name, including)

            self.stdout.write(name_str, ending='')
            if index == 0 and including:
                date_including_str = self.build_date_period(including)
                self.stdout.write(f'   {ITALIC}{date_including_str}{RESET}')
            else:
                self.stdout.write('')
    
    def populate_yname(self, kwargs):
        if self.yname:
            kwargs['start_year__lte'] = self.yname
            kwargs['end_year__gte'] = self.yname

    def handle(self, *args, **options):
        unit_id = options['unit-id'][0]
        self.yname = options['yname']

        kwargs = {}
        self.populate_yname(kwargs)

        unit = Unit.objects.filter(id=unit_id).first()
        if not unit:
            self.stdout.write('АТЕ не найдена')
            return

        self.stdout.write(f'{BOLD}Наименования:{RESET}')
        self.print_names(unit)

        date_period = self.build_date_period(unit)
        date_period = date_period if date_period else '-'
        self.stdout.write(f'\n{BOLD}Годы существования:{RESET} {date_period}')

        self.stdout.write(f'\n{BOLD}Включает:{RESET}')
        for including in unit.children_includings.all():
            self.print_names(including.child, including)

        self.stdout.write(f'\n{BOLD}Входит в:{RESET}')
        for including in unit.parent_includings.all():
            self.print_names(including.parent, including)
