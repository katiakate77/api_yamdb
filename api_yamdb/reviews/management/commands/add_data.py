import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


class Command(BaseCommand):
    """
    Добавляет данные из csv файлов в модели.
    Для запуска скрипта: python api_yamdb/manage.py add_data [модель]
    """

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='model')

    def handle(self, *args, **options):
        dir_path = os.path.abspath(
            os.path.join('.', 'api_yamdb', 'static', 'data')
        )

        path_and_model = {
            'category': {'category.csv': Category},
            'comments': {'comments.csv': Comment},
            'genre_title': {'genre_title.csv': GenreTitle},
            'genre': {'genre.csv': Genre},
            'review': {'review.csv': Review},
            'titles': {'titles.csv': Title},
            'users': {'users.csv': User},
        }

        if options['model'].lower() in path_and_model:
            obj = path_and_model[options['model'].lower()]
            file = list(obj.keys())[0]
            path = os.path.join(dir_path, file)
            model = list(obj.values())[0]

            obj_list = []
            with open(path, encoding='utf-8') as csv_file:
                for obj_dict in csv.DictReader(csv_file):
                    if options['model'].lower() == 'titles':
                        obj_dict['category'] = Category(
                            int(obj_dict['category'])
                        )
                    elif options['model'].lower() == 'review':
                        obj_dict['author'] = User(int(obj_dict['author']))
                    elif options['model'].lower() == 'comments':
                        obj_dict['author'] = User(int(obj_dict['author']))
                    obj_list.append(model(**obj_dict))
                model.objects.bulk_create(obj_list)
        else:
            raise Exception('Такой модели нет')

