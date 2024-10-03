from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters, permissions, viewsets, serializers, status
)
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title
from .mixins import CategoryGenreMixin
from .filters import TitleFilter
from .permissions import AdminModeratorAuthor, IsAdmin, IsAdminOrReadOnly
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, ReviewSerializer,
    SignupSerializer, TitleSerializerForRead, TitleSerializerForWrite,
    TokenSerializer, UserSerializer
)
from .utils import get_confirmation_code

User = get_user_model()


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            try:
                current_user, current_status = User.objects.get_or_create(
                    email=email,
                    username=username
                )
            except IntegrityError:
                raise serializers.ValidationError(
                    'Такой пользователь уже зарегистрирован!')
            current_user.confirmation_code = get_confirmation_code()
            send_mail(
                subject='Код подтверждения',
                message=current_user.confirmation_code,
                from_email='example@ex.ru',
                recipient_list=(email,)
            )
            current_user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(APIView):
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
    search_fields = ('username',)
    permission_classes = (IsAdmin,)

    @action(methods=('get', 'patch'), detail=False, url_path='me',
            permission_classes=(permissions.IsAuthenticated,))
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


class CategoryViewSet(CategoryGenreMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering_fields = ('id', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSerializerForWrite
        return TitleSerializerForRead


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthor,)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthor,)

    def get_queryset(self):
        return self.get_review().comments.all()

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review(),)
