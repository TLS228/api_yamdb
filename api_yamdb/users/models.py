from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = (
    ('user', 'обычный'),
    ('moderator', 'модератор'),
    ('admin', 'администратор')
)


class MyUser(AbstractUser):
    bio = models.CharField(max_length=256, blank=True)
    role = models.CharField(max_length=16, choices=CHOICES, default='user')
