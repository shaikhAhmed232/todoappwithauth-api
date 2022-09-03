from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED)

from .models import TodoItem

# Create your tests here.
class TestTodo(APITestCase):
    todo_list_url = reverse("get_todo_list")
    todo_item_url = reverse("single_todo_item", kwargs={"pk": 1})
    dummy_todo_data = {
        "title": "dummy_task_title",
        "task": "dummy_task_title",
        "todo_list": 1, 
    } 

    def authenticate(self):
        url = reverse("login")
        user = User.objects.create_user(username="test_username", email="testemail@mail.com", password="testpassword")
        response = self.client.post(url, {"username": "test_username", "password": "testpassword"})
        tokens = response.data["tokens"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + tokens["access"])

    def test_unauthorized_user_get_todo_list(self):
        response = self.client.get(self.todo_list_url)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_authorized_user_get_todo_list(self):
        self.authenticate()
        response = self.client.get(self.todo_list_url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_unauthorized_user_not_allowed_create_todo(self):
        response = self.client.post(self.todo_list_url, self.dummy_todo_data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_authorized_user_allowed_create_todo(self):
        self.authenticate()
        tasks = TodoItem.objects.all().count()
        response = self.client.post(self.todo_list_url, self.dummy_todo_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(TodoItem.objects.all().count(), tasks + 1)

    def test_unauthorized_user_retrieving_single_todo_item(self):
        response = self.client.get(self.todo_item_url, {"pk": 1})
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_authorized_user_retrieving_single_todo_item(self):
        self.authenticate()
        response = self.client.get(self.todo_item_url)
        self.assertEqual(response.status_code, HTTP_200_OK)


        

