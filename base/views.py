from urllib import request
from wsgiref.util import request_uri
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task, ToDoList


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('lists')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('lists')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class ToDoListList(LoginRequiredMixin, ListView):
    model = ToDoList
    context_object_name = "lists"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lists'] = context['lists'].filter(user=self.request.user)
        context['count'] = context['lists'].count

        search_input = self.request.GET.get('search-area') or ''

        if search_input:
            context['lists'] = context['lists'].filter(title__icontains=search_input)

        context['search_input'] = search_input

        return context


class TodoListCreate(LoginRequiredMixin, CreateView):
    model = ToDoList
    fields = ['title']
    success_url = reverse_lazy('lists')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoListCreate, self).form_valid(form)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(list=self.kwargs['list'])
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count

        search_input = self.request.GET.get('search-area') or ''

        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "base/task.html"


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']

    def get_success_url(self):
        return reverse_lazy('tasks', kwargs={'list': self.kwargs['list']})

    def form_valid(self, form):
        form.instance.user = self.request.user
        print(self.kwargs['list'])
        form.instance.list = ToDoList.objects.get(id=self.kwargs['list'])

        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']

    def get_success_url(self):
        return reverse_lazy('tasks', kwargs={'list': self.kwargs['list']})


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'

    def get_success_url(self):
        return reverse_lazy('tasks', kwargs={'list': self.kwargs['list']})
