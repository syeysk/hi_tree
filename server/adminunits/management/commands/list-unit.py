from os import SEEK_CUR

from django.core.management.base import BaseCommand
# from django.db import

from adminunits.models import UnitName


class Command(BaseCommand):
    help = 'Manipulate your historical administrative units'

    def add_arguments(self, parser):
        parser.add_argument('--yname', nargs='?', type=int)

    def build_date_period(self, obj_with_date):
        if obj_with_date.start_date and obj_with_date.end_date:
            return f'{obj_with_date.start_date} - {obj_with_date.end_date}'
        elif obj_with_date.start_date:
            return f'с {obj_with_date.start_date}'
        elif obj_with_date.end_date:
            return f'по {obj_with_date.end_date}'
        
        return '' 

    def build_name(self, unit_name):
        dates_str = self.build_date_period(unit_name)
        if dates_str:
            dates_str = f' ({dates_str})'

        unit_name_id_str = str(unit_name.id).rjust(2, '0')
        unit_id_str = str(unit_name.unit.id).rjust(2, '0')

        return f'{unit_id_str}.{unit_name_id_str} {unit_name.name}{dates_str}'
    
    def print_names(self, unit, deep_level, including):
        kwargs = {}
        if self.yname:
            kwargs['start_year__lt'] = self.yname
            kwargs['end_year__gt'] = self.yname

        for index, unit_name in enumerate(UnitName.objects.filter(unit=unit, **kwargs).all()):
            name_str = self.build_name(unit_name)
            for _ in range(deep_level):
                self.stdout.write('  ', ending='')

            self.stdout.write(name_str, ending='')
            if index == 0 and deep_level > 0:
                date_including_str = self.build_date_period(including)
                self.stdout.write(f'. Входила {date_including_str} (ID вхождения: {including.id})')                
            else:
                self.stdout.write('')

    def print_children(self, parent_unit, deep_level=0, parent_including=None):
        if parent_unit.id not in self.not_print_ids:
            self.print_names(parent_unit, deep_level, parent_including)
            self.not_print_ids.add(parent_unit.id)

        deep_level += 1
        for including in parent_unit.parent_includings.all():
            self.print_children(including.child, deep_level, including)

    def handle(self, *args, **options):
        # self.max_count_digits_in_unit_name_id = Unit.objects.first(id=)
        self.yname = options['yname']
        self.not_print_ids = set()

        kwargs = {}
        if self.yname:
            kwargs['start_year__lt'] = self.yname
            kwargs['end_year__gt'] = self.yname

        unit_names = UnitName.objects.filter(**kwargs).all()
        for unit_name in unit_names:
            self.print_children(unit_name.unit)

