from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Title, Review, Comment, Genre, Category

User = get_user_model()


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category')
    search_fields = ('name', 'year')
    list_filter = ('year',)
    empty_value_display = '-empty-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(User)
