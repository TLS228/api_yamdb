from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator, MinValueValidator
)


MAX_USERNAME_LENGTH = 150
MAX_EMAIL_LENGTH = 254
MAX_PASSWORD_LENGTH = 128
MIN_PASSWORD_LENGTH = 8
MAX_BIO_LENGTH = 256
MAX_NAME_LENGTH = 256
MAX_SLUG_LENGTH = 50
MAX_TEXT_LENGTH = 1000
MIN_SCORE = 1
MAX_SCORE = 10
CHOICES = (
    ('user', 'обычный'),
    ('moderator', 'модератор'),
    ('admin', 'администратор')
)


class MyUser(AbstractUser):
<<<<<<< HEAD
    email = models.EmailField(max_length=254,
                              unique=True,
                              verbose_name='Почта')
    bio = models.CharField(max_length=256, blank=True,
                           verbose_name='Биография')
    role = models.CharField(max_length=16, choices=CHOICES,
                            default='user', verbose_name='Роль')
    confirmation_code = models.CharField(max_length=6, blank=True, null=True,
                                         verbose_name='Код подтверждения')
    username = models.CharField(max_length=150, unique=True)
=======
    email = models.EmailField(
        max_length=MAX_EMAIL_LENGTH, unique=True,
        verbose_name='Почта'
    )
    bio = models.CharField(
        max_length=MAX_BIO_LENGTH, blank=True, verbose_name='Биография')
    role = models.CharField(
        max_length=MAX_NAME_LENGTH, choices=CHOICES,
        default='user', verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        max_length=MAX_PASSWORD_LENGTH, blank=True, null=True,
        verbose_name='Код подтверждения'
    )
>>>>>>> a166a094997e771170a1f9476a370f26cbfc450f

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField('Категория', max_length=MAX_NAME_LENGTH)
    slug = models.SlugField('Слаг', max_length=MAX_SLUG_LENGTH, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=MAX_NAME_LENGTH)
    slug = models.SlugField('Слаг', max_length=MAX_SLUG_LENGTH, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=MAX_NAME_LENGTH)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='category',
        null=True, verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField('Текст отзыва', max_length=MAX_TEXT_LENGTH)
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE),
        ],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField('Текст комментария', max_length=MAX_TEXT_LENGTH)
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
