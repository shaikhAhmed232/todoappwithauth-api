from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from .models import TodoList, TodoItem
from .serializers import TodoListSerializer, TodoItemSerializer

# Create your views here.
class Todo(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = request.user
        todo_list = TodoList.objects.prefetch_related("tasks").filter(owner=user)
        if not todo_list.exists():
            return Response({'msg': 'you have no todo list! Please Login again to get one.'}, status=HTTP_404_NOT_FOUND)
        serializer = TodoListSerializer(todo_list[0])
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        user = request.user
        todo_list = user.todo_list
        data = request.data
        serializer = TodoItemSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        serializer.save(todo_list=todo_list)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete(self, request):
        user = request.user
        todo_list = user.todo_list
        todo_list.tasks.all().delete()
        return Response(status=HTTP_200_OK)         

class SingleTodoItem(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        todo_item = TodoItem.objects.filter(pk=pk)
        if not todo_item.exists():
            return Response(status=HTTP_404_NOT_FOUND)

        todo_item = todo_item[0]
        serializer = TodoItemSerializer(todo_item)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):
        todo_item = TodoItem.objects.filter(pk=pk)
        if not todo_item.exists():
            return Response(status=HTTP_404_NOT_FOUND)

        data = request.data
        todo_item = todo_item[0]
        serializer = TodoItemSerializer(instance=todo_item, data=data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)

    def delete(self, request, pk):
        todo_item = TodoItem.objects.filter(pk=pk)
        if not todo_item.exists():
            return Response(status=HTTP_404_NOT_FOUND)

        todo_item[0].delete()
        return Response({"msg": "Task Deleted Successfully"}, status=HTTP_200_OK)


