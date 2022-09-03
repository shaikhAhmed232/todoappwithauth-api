from unittest.util import _MAX_LENGTH
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import TodoItem, TodoList

class TodoItemSerializer(serializers.ModelSerializer):
    # owner_username = serializers.CharField(required=False, max_length=100)
    class Meta:
        model = TodoItem
        fields = ('id', 'title', 'task', 'completed', 'created', 'todo_list')
        extra_kwargs = {"todo_list": {"read_only": True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner_username'] = instance.todo_list.owner.username
        return representation

    def validate(self, data):
        task = data['task']
        title = data['title']
        if len(task) == 0:
            raise ValidationError('Please provide proper task.')
        if len(title) == 0:
            raise ValidationError('Please give title your task.')

        return data

    def update(self, instance, validated_data):
        instance.task = validated_data["task"]
        instance.title = validated_data["title"]
        instance.completed = validated_data["completed"]
        instance.save()
        return instance

class TodoListSerializer(serializers.ModelSerializer):
    tasks = TodoItemSerializer(read_only=True, many=True)
    class Meta:
        model = TodoList
        fields = ('owner', 'tasks')

