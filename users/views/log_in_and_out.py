from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import render

from users.forms import LoginForm


class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Logging in'
        return context


class LogoutView(BaseLogoutView):
    pass


def login_warning(request):
    context = {'page_title': 'Logging in warning'}
    return render(request, 'users/login_warning.html', context)
