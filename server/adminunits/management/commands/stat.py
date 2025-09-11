from os import SEEK_CUR

from django.core.management.base import BaseCommand, CommandError
# from django.db import

from adminunits.models import UnitName, Including, Unit


class Command(BaseCommand):
    help = 'Manipulate your historical administrative units'

    def handle(self, *args, **options):
        total_units = 0
        total_name_units = 0
        total_includings = 0
        self.stdout.write(f'Всего')
        self.stdout.write(f'  АТЕ: {total_units}')
        self.stdout.write(f'  наименований АТЕ: {total_name_units}')
        self.stdout.write(f'  включений АТЕ: {total_includings}')
        self.stdout.write(f'АТЕ без наименования:')
