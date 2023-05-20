from django.http import HttpResponse
from rest_framework import serializers

from rest_framework.generics import CreateAPIView

from auth_user.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """
    Create a new user
    """
    serializer_class = UserSerializer
