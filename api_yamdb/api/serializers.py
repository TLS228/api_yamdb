from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from django.core.mail import send_mail

from .mixins import UsernameFieldMixin
from reviews.models import (
    Category, Comment, Genre, Review, Title,
    MAX_EMAIL_LENGTH, CONFIRMATION_CODE_LENGTH
)

User = get_user_model()

ERROR_MSG = 'Такой пользователь уже зарегистрирован!'
SUBJECT = 'Код подтверждения'
FROM_EMAIL = 'example@ex.ru'
USER_ALREADY_REVIEWED = 'Вы уже оставляли отзыв к этому произведению!'
USER_CREATION_ERROR = 'Ошибка при создании пользователя!'
CONFIRMATION_CODE_LENGTH = 6
TOKEN_ERROR = {'confirmation_code': 'Неверный код подтверждения!'}


class SignupSerializer(UsernameFieldMixin):
    email = serializers.EmailField(max_length=MAX_EMAIL_LENGTH, required=True)

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        try:
            current_user, current_status = User.objects.get_or_create(
                email=email,
                username=username
            )
        except IntegrityError:
            raise serializers.ValidationError(ERROR_MSG)
        send_mail(
            subject=SUBJECT,
            message=current_user.confirmation_code,
            from_email=FROM_EMAIL,
            recipient_list=(email,)
        )
        return current_user


class TokenSerializer(UsernameFieldMixin):
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH, required=True
    )

    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError(TOKEN_ERROR)
        return data

class UserSerializer(serializers.ModelSerializer, UsernameFieldMixin):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

    def create(self, validated_data):
        try:
            user = User.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(USER_CREATION_ERROR)
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializerForRead(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        scores = Review.objects.filter(title=obj).values_list('score',
                                                              flat=True)

        return round(sum(scores) / len(scores)) if scores else None


class TitleSerializerForWrite(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=True,
        allow_null=False,
        allow_empty=False
    )

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, instance):
        serializer = TitleSerializerForRead(instance)
        return serializer.data


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
            raise serializers.ValidationError(USER_ALREADY_REVIEWED)
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
