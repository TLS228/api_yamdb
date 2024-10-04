import csv

from django.core.management.base import BaseCommand

from reviews.models import (
    Category, Comment, Genre, GenreTitle, MyUser, Review, Title,
)


class Command(BaseCommand):
    help = 'Импортирует данные из CSV-файлов'

    def handle(self, *args, **options):
        self.import_users()
        self.import_category()
        self.import_genres()
        self.import_titles()
        self.import_review()
        self.import_comments()
        self.import_genre_title()

    def import_from_csv(self, model, filename):
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'author' in row:
                    row['author'] = MyUser.objects.get(id=row['author'])
                if 'category' in row:
                    row['category'] = Category.objects.get(id=row['category'])
                obj, created = model.objects.get_or_create(**row)
                if created:
                    obj.save()
            self.stdout.write(
                self.style.SUCCESS(f'{model.__name__} импортированы успешно')
            )

    def import_users(self):
        self.import_from_csv(MyUser, 'static/data/users.csv')

    def import_category(self):
        self.import_from_csv(Category, 'static/data/category.csv')

    def import_genres(self):
        self.import_from_csv(Genre, 'static/data/genre.csv')

    def import_titles(self):
        self.import_from_csv(Title, 'static/data/titles.csv')

    def import_review(self):
        self.import_from_csv(Review, 'static/data/review.csv')

    def import_comments(self):
        self.import_from_csv(Comment, 'static/data/comments.csv')

    def import_genre_title(self):
        self.import_from_csv(GenreTitle, 'static/data/genre_title.csv')
