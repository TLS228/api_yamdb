from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = (
    ('user', 'обычный'),
    ('moderator', 'модератор'),
    ('admin', 'администратор')
)


class MyUser(AbstractUser):
    bio = models.CharField(max_length=256, blank=True,
                           verbose_name='Биография')
    role = models.CharField(max_length=16, choices=CHOICES,
                            default='user', verbose_name='Роль')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Title(models.Model):
    pass


class Category(models.Model):
    pass


class Genre(models.Model):
    pass


class Review(models.Model):  #делаю я
    pass


class Comment(models.Model):  #делаю я
    pass
