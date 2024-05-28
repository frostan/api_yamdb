import csv

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ('Загружает данные из csv файлов в sqlite.\n'
            'Пример команды: '
            'python manage.py loadcsv static/data/titles.csv reviews Title')

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Путь к файлу')
        parser.add_argument(
            'app_name',
            type=str,
            help='Имя приложения, к которому подключена модель'
        )
        parser.add_argument('model_name', type=str, help='Имя модели')

    def handle(self, *args, **options):
        try:
            file_path = options['path']
            _model = apps.get_model(options['app_name'], options['model_name'])
            with open(file_path, 'r') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                header = next(reader)
                for row in reader:
                    _object_dict = {
                        key: value for key, value in zip(header, row)
                    }
                    _model.objects.update_or_create(**_object_dict)
            self.stdout.write(self.style.SUCCESS('Файл загружен в БД'))
        except LookupError:
            self.stdout.write(self.style.ERROR('Ошибка, не найден файл'))
