from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import serializers, status, views
from rest_framework.response import Response

from .serializers import SignupSerializer

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
