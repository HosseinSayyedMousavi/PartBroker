from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AccountTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('api:v1:accounts:register')
        self.login_url = reverse('api:v1:accounts:login')
        self.user_info_url = reverse('api:v1:accounts:user-info')

        self.user_data = {
            "phone_number": "1234567890",
            "password": "TestPassword123!",
            "password1": "TestPassword123!"
        }


        self.user = User.objects.create_user(
            phone_number="0987654321",
            password="TestPassword123!"
        )

        self.token = RefreshToken.for_user(self.user).access_token

    def test_user_registration(self):
        """Test that a user can register with valid data."""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('phone_number', response.data.keys())
        self.assertNotEqual(self.user_data['password'], response.data['password'])

    def test_user_registration_password_mismatch(self):
        """Test that registration fails when passwords do not match."""
        data = self.user_data.copy()
        data['password1'] = 'DifferentPassword!'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)

    def test_user_registration_invalid_password(self):
        """Test that registration fails with an invalid password."""
        data = self.user_data.copy()
        data['password'] = 'short'
        data['password1'] = 'short'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_login(self):
        """Test that a user can log in and receive a JWT token."""
        response = self.client.post(self.login_url, {
            'phone_number': self.user.phone_number,
            'password': 'TestPassword123!'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_user_info(self):
        """Test retrieving user info with authentication."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], self.user.phone_number)
        self.assertIn('email', response.data)

    def test_get_user_info_unauthenticated(self):
        """Test that unauthenticated access to user info is denied."""
        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_info(self):
        """Test updating user information."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        update_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        response = self.client.put(self.user_info_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'user updated successfully!')

        # Verify the changes
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'john.doe@example.com')

    def test_update_user_info_partial(self):
        """Test partially updating user information."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        update_data = {
            "first_name": "John"
        }
        response = self.client.put(self.user_info_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'user updated successfully!')

        # Verify the changes
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, None)  # No change since it wasn't updated

    def test_update_user_info_unauthenticated(self):
        """Test that unauthenticated update of user info is denied."""
        update_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        response = self.client.put(self.user_info_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
