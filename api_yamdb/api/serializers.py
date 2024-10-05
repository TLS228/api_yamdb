from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from reviews.constants import (
    CONFIRMATION_CODE_LENGTH, FROM_EMAIL, MAX_EMAIL_LENGTH, SUBJECT,
    TOKEN_ERROR_MESSAGE, USER_ALREADY_REVIEWED_MESSAGE, USERNAME_ERROR_MESSAGE
)
from reviews.models import Category, Comment, Genre, Review, Title
from .mixins import UsernameFieldMixin, UsernameValidatorMixin

User = get_user_model()


class SignupSerializer(UsernameFieldMixin):
    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        required=True
    )

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        try:
            current_user, current_status = User.objects.get_or_create(
                email=email,
                username=username
            )
        except IntegrityError:
            raise serializers.ValidationError(USERNAME_ERROR_MESSAGE)
        send_mail(
            subject=SUBJECT,
            message=current_user.confirmation_code,
            from_email=FROM_EMAIL,
            recipient_list=(email,)
        )
        return current_user


class TokenSerializer(UsernameFieldMixin):
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        required=True
    )

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError(TOKEN_ERROR_MESSAGE)
        return data


class UserSerializer(UsernameValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


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
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('rating') is None:
            representation['rating'] = None
        return representation


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
            raise serializers.ValidationError(USER_ALREADY_REVIEWED_MESSAGE)
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
