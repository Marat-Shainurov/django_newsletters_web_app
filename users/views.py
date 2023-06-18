from django.shortcuts import render
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.views import generic

from users.forms import UserRegisterForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'

class LogoutView(BaseLogoutView):
    pass

class RegisterView(generic.CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')