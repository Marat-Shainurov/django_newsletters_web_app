import random

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy, reverse
from django.views import generic

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserListView(generic.ListView):
    model = User

class UserUpdateView(generic.UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:user_list')

class LoginView(BaseLoginView):
    template_name = 'users/login.html'

class LogoutView(BaseLogoutView):
    pass


class RegisterView(generic.CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        self.object = form.save()
        if form.is_valid():
            code = ''.join([str(random.randint(0,9)) for _ in range(12)])
            self.object.verification_code = code
            self.object.save()
            send_mail(
                'Email verification',
                f'Your verification code - {code}. Please, use it for logging in.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.object.email]
            )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:verify_email', kwargs={'email': self.object.email})

def verify_email(request, email):
    if request.method == 'POST':
        code = request.POST.get('code')
        user = User.objects.get(email=email)
        if user.verification_code == code:
            user.is_verified = True
            user.save()
            return redirect(reverse('users:login'))
        else:
            raise ValidationError('You have inputted the wrong verification code')
    else:
        return render(request, 'users/verify_email.html')