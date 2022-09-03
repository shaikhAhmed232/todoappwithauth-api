from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TodoList(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="todo_list")
    
    def __str__(self):
        return f"{self.owner.username}'s todo list."

class TodoItem(models.Model):
    title = models.CharField(max_length=100)
    task = models.CharField(max_length=500)
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="tasks")
    completed = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering=("-created",)
