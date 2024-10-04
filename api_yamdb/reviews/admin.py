from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Title, Review, Comment, Genre, Category


User = get_user_model()

admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(User)
