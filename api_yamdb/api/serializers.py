from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db.utils import IntegrityError
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
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

    def create(self, validated_data):
        try:
            user = User.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError('Ошибка при создании пользователя!')
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def get_rating(self, obj):
        scores = Review.objects.filter(title=obj).values_list('score', flat=True)
        return round(sum(scores) / len(scores)) if scores else None





class TitleSerializerForRead(serializers.ModelSerializer):
    """Сериализатор данных модели произведения для чтения."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        scores = Review.objects.filter(title=obj).values_list('score', flat=True)
        return round(sum(scores) / len(scores)) if scores else None


class TitleSerializerForWrite(serializers.ModelSerializer):
    """Сериализатор данных модели произведения для записи."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug',
        allow_null=False,
        allow_empty=False
    )

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, instance):
        return TitleSerializerForRead(instance).data












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
