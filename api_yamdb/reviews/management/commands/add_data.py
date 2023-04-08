from csv import DictReader
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title, GenreTitle, Comment, Review
from users.models import User


class Command(BaseCommand):
    """
    Добавляет данные из csv файлов в модели.
    Для запуска скрипта: python api_yamdb/manage.py add_data
    """

    def handle(self, *args, **options):
        for row in DictReader(open('./api_yamdb/static/data/users.csv',
                                   errors='ignore', encoding='utf-8')):
            user = User(
                id=row['id'], username=row['username'],
                email=row['email'], role=row['role'],
                bio=row['bio'], first_name=row['first_name'],
                last_name=row['last_name']
            )
            user.save()
        for row in DictReader(open('./api_yamdb/static/data/category.csv',
                                   errors='ignore', encoding='utf-8')):
            category = Category(
                id=row['id'], name=row['name'], slug=row['slug']
            )
            category.save()
        for row in DictReader(open('./api_yamdb/static/data/genre.csv',
                                   errors='ignore', encoding='utf-8')):
            genre = Genre(
                id=row['id'], name=row['name'], slug=row['slug']
            )
            genre.save()
        for row in DictReader(open('./api_yamdb/static/data/titles.csv',
                                   errors='ignore', encoding='utf-8')):
            title = Title(
                id=row['id'], name=row['name'],
                year=row['year'], category_id=row['category']
            )
            title.save()
        for row in DictReader(open('./api_yamdb/static/data/review.csv',
                                   errors='ignore', encoding='utf-8')):
            review = Review(
                id=row['id'], title_id=row['title_id'],
                text=row['text'], author_id=row['author'],
                score=row['score'], pub_date=row['pub_date']
            )
            review.save()
        for row in DictReader(open('./api_yamdb/static/data/comments.csv',
                                   errors='ignore', encoding='utf-8')):
            comment = Comment(
                id=row['id'], review_id=row['review_id'],
                text=row['text'], author_id=row['author'],
                pub_date=row['pub_date']
            )
            comment.save()
        for row in DictReader(open('./api_yamdb/static/data/genre_title.csv',
                                   errors='ignore', encoding='utf-8')):
            genre_title = GenreTitle(
                id=row['id'], title_id=row['title_id'],
                genre_id=row['genre_id']
            )
            genre_title.save()
