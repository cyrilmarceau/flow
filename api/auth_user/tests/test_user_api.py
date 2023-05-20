"""
Tests for the user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('auth_user:create')


def create_user(**params):
    """
    Helper function to create a user
    """

    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    Test the users API (public)
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        Test creating user with valid payload is successful
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass',
            'password_confirm': 'testpass',
            'username': 'test',
            'phone': '0102030405',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=res.data['email'])

        self.assertTrue(user.check_password(payload['password']))

        # Verify that the password is not returned in the response
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """
        Test creating a user that already exists fails
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass',
            'username': 'test',
            'phone': '0102030405',
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test that the password must be more than 5 characters
        """
        payload = {
            'email': 'test@example.com',
            'password': 'shor',
            'username': 'test',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify that the user was not created
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exist)

    def test_passwords_dont_match(self):
        """
        Test that the passwords must match
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass',
            'password_confirm': 'testpass2',
            'username': 'test',
            'phone': '0102030405',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)




