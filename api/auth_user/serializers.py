"""
Serializers for the auth_user app.
"""
import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'phone', 'password_confirm')
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

    def create(self, validated_data):
        """
        Create a new user and return it.
        """

        validated_data.pop('password_confirm', None)

        return get_user_model().objects.create_user(**validated_data)
