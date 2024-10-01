from django.db import models
from django.contrib.auth.models import AbstractUser


CHOICES = (
    ('user', 'обычный'),
    ('moderator', 'модератор'),
    ('admin', 'администратор')
)


class MyUser(AbstractUser):
    bio = models.CharField(max_length=256, blank=True)
    role = models.CharField(max_length=16, choices=CHOICES, default='user')


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
