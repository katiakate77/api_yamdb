import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Genre, Title, GenreTitle
from users.models import User
from django.db.models.fields.related import ForeignKey


class Command(BaseCommand):
    """
    Наполняет базу данных данными из csv файла.
    python api_yamdb/manage.py add_data [путь до файла] [название модели].
    """

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)
        parser.add_argument('model_name', type=str)

    def handle(self, *args, **options):
        df = pd.read_csv(options['file_path'])
        row_iter = df.iterrows()
        model = self.get_model(options['model_name'])

        objs = []
        for index, row in row_iter:
            data = row.to_dict()
            for field_name, value in data.items():
                field = model._meta.get_field(field_name)
                if isinstance(field, ForeignKey):
                    related_model = field.related_model
                    if options['model_name'].lower() == 'genre_title':
                        data[field_name] = value
                    else:
                        data[field_name] = related_model.objects.get(pk=value)
            obj = model.objects.create(**data)
            objs.append(obj)

    def get_model(self, model_name):
        models = {
            'category': Category,
            'genre': Genre,
            'title': Title,
            'genre_title': GenreTitle,
            'user': User
        }
        try:
            return models[model_name.lower()]
        except KeyError:
            raise CommandError(f'Invalid model name: {model_name}')
