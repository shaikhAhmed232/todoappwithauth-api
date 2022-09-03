from django.contrib.auth.models import User 
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class TestAccount(APITestCase):
    def test_account_signup(self):
        url = reverse("signup")
        data = {
            "username": "test_user",
            "email": "testpassword@mail.com",
            "password": "test_password"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticate_user(self):
        url = reverse("login")
        user = User.objects.create_user(username="test_user", email="testuser@mail.com", password="testpassword")
        data = {
            "username": "test_user",
            "password": "testpassword"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def authenticate(self):
        url = reverse("login")
        user = User.objects.create_user(username="test_username", email="testemail@mail.com", password="testpassword")
        data = {
            "username": "test_username",
            "password": "testpassword"
        }

        response = self.client.post(url, data)
        tokens = response.data["tokens"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + tokens["access"])

    def test_unauthorized_get_current_user(self):
        url = reverse("current_user")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_get_current_user(self):
        self.authenticate()
        url = reverse("current_user")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
