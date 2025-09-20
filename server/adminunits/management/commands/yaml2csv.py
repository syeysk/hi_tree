import csv
import yaml
from pathlib import Path

from django.core.management.base import BaseCommand

base_path = Path(__file__).parent.parent.parent.parent.parent
data_path = base_path / 'data'
yaml_path = base_path / 'server' / 'data.yaml'
model_order_path = data_path / 'model_order.csv'


def modify_fields_to_csv(fields, model):
    if model == 'adminunits.unit':
        point = fields.pop('point')
        fields['lon'], fields['lat'] = point[17:-1].split() if point else (None, None)
        print(point, fields['lon'], fields['lat'])


def modify_fields_from_csv(fields, model):
    if model == 'adminunits.unit':
        lon = fields.pop('lon')
        lat = fields.pop('lat')
        fields['point'] = f'SRID=4326;POINT ({lon} {lat})' if lon and lat else None


class Command(BaseCommand):
    help = 'Manipulate your historical administrative units'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--reverse', action='store_true')

    @staticmethod
    def write_model_order(models: list[str]):
        with open(model_order_path, mode='wt', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(models)

    @staticmethod
    def read_model_order() -> list[str]:
        with model_order_path.open() as model_order_file:
            for row in csv.reader(model_order_file):
                return row

    def handle(self, *args, **options):
        if options['reverse']:
            yaml_data = []
            for model in self.read_model_order():
                with (data_path / f'{model}.csv').open('rt', encoding='utf-8') as csv_file:
                    csv_reader = csv.reader(csv_file, lineterminator='\n')
                    field_names = None
                    for row_index, row in enumerate(csv_reader):
                        if not row:
                            continue

                        if not row_index:
                            field_names = row
                            continue

                        row = [value if value else None for value in row]
                        yaml_data.append({
                            'model': model,
                            'pk': row[0],
                            'fields': dict(zip(field_names[1:], row[1:]))
                        })
                        modify_fields_from_csv(yaml_data[-1]['fields'], model)
            
            with yaml_path.open('wt', encoding='utf-8') as yaml_file:
                yaml.safe_dump(yaml_data, yaml_file, allow_unicode=True, encoding='utf-8', sort_keys=False)
        else:
            with open(yaml_path, 'rt', encoding='utf-8') as file:
                yaml_data = yaml.safe_load(file)

            current_model, csv_writer, csv_file, fields_by_order = None, None, None, None
            models = []
            for yaml_row in yaml_data:
                model = yaml_row['model']
                fields = {'pk': yaml_row['pk'], **yaml_row['fields']}
                modify_fields_to_csv(fields, model)
                if model != current_model:
                    if csv_file:
                        csv_file.close()

                    current_model = model
                    csv_file = open(data_path / f'{model}.csv', mode='wt', encoding='utf-8')
                    csv_writer = csv.writer(csv_file, lineterminator='\n')
                    fields_by_order = fields.keys()
                    self.stdout.write(f'Ready model: {current_model}')
                    csv_writer.writerow(fields_by_order)
                    models.append(model)
                
                csv_writer.writerow([fields[field] for field in fields_by_order])

            self.write_model_order(models)
