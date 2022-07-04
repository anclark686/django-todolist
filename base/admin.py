from django.contrib import admin
from .models import Task, ToDoList


admin.site.register(Task)
admin.site.register(ToDoList)
