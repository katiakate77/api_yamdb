import os
import csv
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title, GenreTitle, Comment, Review
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
            os.path.join(".", "api_yamdb", "static", "data")
        )

        path_and_model = {
            'users': {os.path.join(dir_path, "users.csv"): User},
            'category': {os.path.join(dir_path, "category.csv"): Category},
            'genre': {os.path.join(dir_path, "genre.csv"): Genre},
            'titles': {os.path.join(dir_path, "titles.csv"): Title},
            'genre_title': {os.path.join(
                            dir_path, "genre_title.csv"): GenreTitle},
            'review': {os.path.join(dir_path, "review.csv"): Review},
            'comments': {os.path.join(dir_path, "comments.csv"): Comment},
        }

        data = []
        if options['model'].lower() in path_and_model:
            obj = path_and_model[options['model'].lower()]
            path = list(obj.keys())[0]
            model = list(obj.values())[0]

            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    data.append(row)
                for item in data[1:]:
                    obj_dict = {key: value for key,
                                value in zip(data[0], item)}
                    if options['model'].lower() == 'titles':
                        obj_dict['category'] = Category(
                            int(obj_dict['category'])
                        )
                    elif options['model'].lower() == 'review':
                        obj_dict['author'] = User(int(obj_dict['author']))
                    elif options['model'].lower() == 'comments':
                        obj_dict['author'] = User(int(obj_dict['author']))
                    obj_item = model(**obj_dict)
                    obj_list = [obj_item]
                    model.objects.bulk_create(obj_list)
        else:
            raise Exception('Такой модели нет')
