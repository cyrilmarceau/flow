"""
Serializers for the auth_user app.
"""
import logging

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from versatileimagefield.serializers import VersatileImageFieldSerializer

from app.settings import UPLOAD_FILE_SIZE_LIMIT
logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    password_confirm = serializers.CharField(write_only=True)
    avatar = VersatileImageFieldSerializer(
        sizes='avatar',
        required=False
    )

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'phone', 'avatar', 'password_confirm')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def validate(self, attrs):
        """
        Validate the password.
        """

        password = attrs.get('password', None)
        password_confirm = attrs.get('password_confirm', None)

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Les deux mots de passe ne correspondent pas.")

        return super().validate(attrs)

    def validate_avatar(self, value):
        """
        Validate the avatar.
        """

        if value:
            if value.size > UPLOAD_FILE_SIZE_LIMIT.get('avatar', 1024 * 1024 * 3):
                raise ValidationError("L'image ne doit pas dépasser 3 Mo.")
            return value
        return None


    def create(self, validated_data):
        """
        Create a new user and return it.
        """

        validated_data.pop('password_confirm', None)

        user = get_user_model().objects.create_user(**validated_data)

        return user
