from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

from .serializers import SignupSerializer

User = get_user_model()


class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
