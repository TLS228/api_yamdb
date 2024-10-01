from django.contrib import admin

from .models import Title, Review, Comment, Genre, Category


admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Category)
