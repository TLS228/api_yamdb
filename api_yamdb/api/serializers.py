from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers
from reviews.models import (
    Category, Comment, MyUser, Genre, Review, Title
)


User = get_user_model()


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')],
        required=True
    )
    email = serializers.EmailField(max_length=254, required=True)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Запрещено использовать это имя!')

        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=6, required=True)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')],
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
            'confirmation_code'
        )


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title_id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв к этому произведению.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
