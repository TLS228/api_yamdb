from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from rest_framework import (
  filters, mixins, permissions, viewsets, generics, serializers, status, views
)
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Title, Review, Comment, Genre, Category
from .permissions import AdminModeratorAuthor, IsAdmin, IsAdminOrReadOnly
from .serializers import (
    ReviewSerializer, CommentSerializer, SignupSerializer, TitleSerializer, 
    TokenSerializer, GenreSerializer, CategorySerializer, UserSerializer
)
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()

NUMS = '1234567890'


def get_confirmation_code(nums=NUMS):
    confirm_code = ''
    nums_set = set(nums)
    for num in nums_set:
        confirm_code += num

    return confirm_code[:6]


class SignupView(views.APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        
        # Проверяем, валидны ли данные запроса
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']

            # Отладка: выводим данные, которые собираемся использовать
            print(f'Attempting to create user with email: {email} and username: {username}')

            # Проверка, существует ли пользователь с таким email
            if User.objects.filter(email=email).exists():
                print(f'User with email {email} already exists.')
                return Response(
                    {'email': 'Пользователь с таким email уже существует!'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Проверка, существует ли пользователь с таким username
            if User.objects.filter(username=username).exists():
                print(f'User with username {username} already exists.')
                return Response(
                    {'username': 'Пользователь с таким username уже существует!'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                # Создание пользователя
                current_user = User.objects.create(
                    email=email,
                    username=username,
                    confirmation_code=get_confirmation_code()
                )

                # Отправка email с кодом подтверждения
                send_mail(
                    subject='Код подтверждения',
                    message=current_user.confirmation_code,
                    from_email='example@ex.ru',
                    recipient_list=[email]
                )

                current_user.save()

                # Отладка: подтверждение успешного создания пользователя
                print(f'User {username} successfully created.')

                return Response(serializer.data, status=status.HTTP_200_OK)

            except IntegrityError as e:
                print(f'IntegrityError occurred: {str(e)}')
                return Response(
                    {'detail': 'Ошибка при создании пользователя.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        else:
            # Если данные невалидны, выводим ошибки сериализатора
            print(f'Invalid data: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(views.APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = serializer.validated_data['confirmation_code']
            username = serializer.validated_data['username']
            user = get_object_or_404(User, username=username)
            if user.confirmation_code != confirmation_code:
                return Response(
                    {"error": "Неверный код подтверждения!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = AccessToken.for_user(user)
            return Response({"token": f"{token}"})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)

    @action(methods=('get', 'patch'), detail=False, url_path='me')
    def current_user_profile(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(role=self.request.user.role)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)


class GenreViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)


class TitleViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)

class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthor,)

    def get_title(self):
        return get_object_or_404(Title,
                                 pk=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthor,)

    def get_review(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review(),
        )

    def get_queryset(self):
        return self.get_review().comments.all()
