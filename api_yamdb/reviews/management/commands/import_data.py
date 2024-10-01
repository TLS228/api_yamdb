from django.core.management.base import BaseCommand
import csv
from reviews.models import Title, Review, Comment, Genre, Category, MyUser, GenreTitle


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

    def import_category(self):

        with open('static/data/category.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                category.save()
        self.stdout.write(self.style.SUCCESS('Категории импортированы успешно'))

    def import_comments(self):
        with open('static/data/comments.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                author_id = row['author']
                author = MyUser.objects.get(id=author_id)
                comment = Comment(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author=author,  # Присвоить объект MyUser полю author
                    pub_date=row['pub_date']
                )
                comment.save()
        self.stdout.write(self.style.SUCCESS('Комментраии импортированы успешно'))

    def import_genre_title(self):
        with open('static/data/genre_title.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                genre_title = GenreTitle(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id']
                )
                genre_title.save()
        self.stdout.write(self.style.SUCCESS('Жанры - Произведения импортированы успешно'))

    def import_genres(self):
        with open('static/data/genre.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                genre = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                genre.save()
        self.stdout.write(self.style.SUCCESS('Жанры импортированы успешно'))

    def import_review(self):
        with open('static/data/review.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                author = MyUser.objects.get(id=row['author'])
                review = Review(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author=author,
                    score=row['score'],
                    pub_date=row['pub_date']
                )
                review.save()
        self.stdout.write(self.style.SUCCESS('Отзывы импортированы успешно'))

    def import_titles(self):
        with open('static/data/titles.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = Category.objects.get(id=row['category'])
                title = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=category
                )
                title.save()
        self.stdout.write(self.style.SUCCESS('Произведения импортированы успешно'))

    def import_users(self):
        with open('static/data/users.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user = MyUser(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
                user.save()
        self.stdout.write(self.style.SUCCESS('Пользователи импортированы успешно'))
