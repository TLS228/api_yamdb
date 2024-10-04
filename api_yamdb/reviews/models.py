from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from django.core.validators import (
    MaxValueValidator, MinValueValidator, RegexValidator
)


MAX_STR_LENGTH = 15
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
    (settings.USER, 'обычный'),
    (settings.MODERATOR, 'модератор'),
    (settings.ADMIN, 'администратор')
)
USERNAME_REGEX_ERROR_MESSAGE = 'Имя пользователя не может быть "me"'
USERNAME_ERROR_MESSAGE = 'Пользователь с таким именем уже существует.'


class User(AbstractUser):
    username = models.CharField(
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        verbose_name='Имя пользователя',
        validators=[
            UnicodeUsernameValidator(),
            RegexValidator(
                regex=r'^((?!me).)*$',
                message=USERNAME_REGEX_ERROR_MESSAGE,
            )
        ],
        error_messages={'unique': USERNAME_ERROR_MESSAGE},
    )

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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return self.username[:MAX_STR_LENGTH]


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
        Genre, verbose_name='Жанр'
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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField('Текст отзыва', max_length=MAX_TEXT_LENGTH)
    author = models.ForeignKey(
        User,
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
        User,
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
        return self.text[:MAX_STR_LENGTH]
