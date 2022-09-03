from django.urls import path

from .views import *

urlpatterns = [
    path('todo-list/', Todo.as_view(), name="get_todo_list"),
    path('<int:pk>/', SingleTodoItem.as_view(), name="single_todo_item"),
]