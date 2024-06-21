from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page='login'), name="logout"),
    path('register', RegisterPage.as_view(), name='register'),

    path('', ToDoListList.as_view(), name="lists"),
    path('todolist-create', TodoListCreate.as_view(), name="todolist-create"),
    path('todolists/<int:list>', TaskList.as_view(), name="tasks"),
    path('todolists/<int:list>/create', TaskCreate.as_view(), name="task-create"),
    path('todolists/<int:list>/task/<int:pk>', TaskDetail.as_view(), name="task"),
    path('todolists/<int:list>/task/<int:pk>/update', TaskUpdate.as_view(), name="task-update"),
    path('todolists/<int:list>/task/<int:pk>/delete', TaskDelete.as_view(), name="task-delete"),
]
