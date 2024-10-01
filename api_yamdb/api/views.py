from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import (
  filters, mixins, pagination, permissions, viewsets, generics, serializers, status, views
)
from rest_framework.generics import get_object_or_404

from reviews.models import Title, Review, Comment, Genre, Category
from .permissions import AdminModeratorAuthor
from .serializers import (
    ReviewSerializer, CommentSerializer, SignupSerializer, TitleSerializer, 
    GenreSerializer, CategorySerializer
)


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
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            current_user, current_status = User.objects.get_or_create(
                email=email,
                username=username
            )
            current_user.confirmation_code = get_confirmation_code()
            send_mail(
                subject='Код подтверждения',
                message=current_user.confirmation_code,
                from_email='example@ex.ru',
                recipient_list=(email,)
            )
            current_user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Review.objects.all()
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
    queryset = Comment.objects.all()
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

