from django.test import TestCase
from django.contrib.auth import get_user_model

from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        email = 'test@example.com'
        password = 'Testpass123'

        image_data = BytesIO()
        image_data.write(b'some sample image data')

        mock_image = SimpleUploadedFile("image.jpg", image_data.getvalue(), content_type="image/jpeg")

        extra_fields = {
            'username': 'testuser',
            'phone': '0601020304',
            'avatar': mock_image
        }

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            **extra_fields
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.username, extra_fields['username'])
        self.assertEqual(user.phone, extra_fields['phone'])
        self.assertEqual(user.avatar, extra_fields['avatar'])

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""

        # Generate arrays of emails with base email and normalized email
        emails = [
            ['upper@EXAMPLE.com', 'upper@example.com'],
            ['Test2@EXAMple.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com']
        ]

        for email, expected in emails:
            user = get_user_model().objects.create_user(email, 'password12345')

            self.assertEqual(user.email, expected)

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'password12345')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""

        user = get_user_model().objects.create_superuser(
            'cyril@example.com',
            'password12345'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
