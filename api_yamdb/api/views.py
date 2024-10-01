from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from .permissions import AdminModeratorAuthor
from .serializers import (
    ReviewSerializer,
    CommentSerializer
)
from reviews.models import Title, Review, Comment

from .serializers import SignupSerializer

User = get_user_model()


class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer


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
