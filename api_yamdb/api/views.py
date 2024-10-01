from django.contrib.auth import get_user_model
from rest_framework import filters, mixins, pagination, permissions, viewsets, generics

from .serializers import SignupSerializer

User = get_user_model()


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
