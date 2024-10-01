from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import serializers, views

from .serializers import SignupSerializer

User = get_user_model()

CONFIRMATION_CODE = '1234567890'


def get_confirmation_code(nums):
    confirm_code = ''
    nums_set = set(nums)
    for num in nums_set:
        confirm_code += num

    return int(confirm_code)


class SignupView(views.APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            current_user, status = User.objects.get_or_create(
                email=email,
                username=username
            )
            current_user.confirmation_code = get_confirmation_code(CONFIRMATION_CODE)
            current_user.save()
        else:
            raise serializers.ValidationError(
                'Проверьте корректность введённых данных!')
