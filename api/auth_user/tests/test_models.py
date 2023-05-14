from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        email = 'test@example.com'
        password = 'Testpass123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

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
