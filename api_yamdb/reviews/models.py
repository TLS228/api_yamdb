from django.db import models


class Auth(models.Model):
    pass


class Title(models.Model):
    pass


class Categorie(models.Model):
    pass


class Genre(models.Model):
    pass


class Review(models.Model):
    pass


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.SET_NULL, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
