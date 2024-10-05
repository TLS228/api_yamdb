import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError
from rest_framework.serializers import ValidationError as DRFValidationError

from api.mixins import username_validator
from api.utils import get_confirmation_code
from .constants import (
    ADMIN, CONFIRMATION_CODE_LENGTH, CHOICES, MAX_BIO_LENGTH, MAX_EMAIL_LENGTH,
    MAX_NAME_LENGTH, MAX_SCORE, MAX_STR_LENGTH, MAX_SLUG_LENGTH,
    MAX_USERNAME_LENGTH, MIN_SCORE, MODERATOR, USER,
    USERNAME_ERROR_MESSAGE
)


class User(AbstractUser):
    username = models.CharField(
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        verbose_name='Имя пользователя',
        validators=[username_validator],
        error_messages={'unique': USERNAME_ERROR_MESSAGE},
    )
    email = models.EmailField(
        max_length=MAX_EMAIL_LENGTH, unique=True,
        verbose_name='Почта'
    )
    bio = models.CharField(
        max_length=MAX_BIO_LENGTH, blank=True, verbose_name='Биография'
    )
    role = models.CharField(
        max_length=MAX_NAME_LENGTH, choices=CHOICES,
        default=USER, verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        max_length=CONFIRMATION_CODE_LENGTH, blank=True,
        verbose_name='Код подтверждения'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def save(self, *args, **kwargs):
        self.confirmation_code = get_confirmation_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username[:MAX_STR_LENGTH]


class BaseCategoryGenre(models.Model):
    name = models.CharField('Название', max_length=MAX_NAME_LENGTH)
    slug = models.SlugField('Слаг', max_length=MAX_SLUG_LENGTH, unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)
        verbose_name = 'Базовая модель для категорий и жанров'

    def __str__(self):
        return self.name


class Category(BaseCategoryGenre):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseCategoryGenre):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


def year_validator(value):
    current_year = datetime.date.today().year
    if value > current_year:
        raise ValidationError(f'Год не может быть больше, чем {current_year}')


class Title(models.Model):
    name = models.CharField('Название', max_length=MAX_NAME_LENGTH)
    year = models.SmallIntegerField('Год выпуска', validators=[year_validator])
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
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
    text = models.TextField('Текст отзыва')
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
    text = models.TextField('Текст комментария')
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
