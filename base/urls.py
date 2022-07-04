from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page='login'), name="logout"),
    path('register', RegisterPage.as_view(), name='register'),

    path('', ToDoListList.as_view(), name="lists"),
    path('todolist-create', TodoListCreate.as_view(), name="todolist-create"),
    path('tasks/<list>', TaskList.as_view(), name="tasks"),
    path('task/<int:pk>/', TaskDetail.as_view(), name="task"),
    path('tasks/<list>/create', TaskCreate.as_view(), name="task-create"),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name="task-update"),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name="task-delete"),
]
