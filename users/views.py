import random

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.management import call_command
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy, reverse
from django.views import generic

from newsletter.models import Newsletter
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
            code = ''.join([str(random.randint(0, 9)) for _ in range(12)])
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


def login_warning(request):
    return render(request, 'users/login_warning.html')


def send_newsletter_manager(request):
    if request.method == 'POST':
        newsletter = request.POST.get('newsletter')
        call_command('action_send_newsletter', f'{newsletter}')
        return redirect(reverse('newsletter:newsletter_list'))
    else:
        user = request.user
        all_newsletters = Newsletter.objects.filter(newsletter_user=user)
        context = {'newsletters_list': all_newsletters}
        return render(request, 'users/send_newsletter_manager.html', context)


def launch_regular_manager(request):
    if request == 'POST':
        newsletter = request.POST.get('newsletter')
        call_command('action_launch_regular_newsletter', f'{newsletter}')
        return redirect(reverse('newsletter:newsletter_list'))
    else:
        user = request.user
        all_newsletters = Newsletter.objects.filter(newsletter_user=user)
        context = {'newsletters_list': all_newsletters}
        return render(request, 'users/launch_regular_manager.html', context)


def remove_regular_manager(request):
    if request == 'POST':
        newsletter = request.POST.get('newsletter')
        call_command('action_remove_cronjob', f'{newsletter}')
        return redirect(reverse('newsletter:newsletter_list'))
    else:
        user = request.user
        all_newsletters = Newsletter.objects.filter(newsletter_user=user)
        context = {'newsletters_list': all_newsletters}
        return render(request, 'users/remove_regular_manager.html', context)