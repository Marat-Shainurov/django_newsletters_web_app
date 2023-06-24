import random

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.views import generic

from users.forms import UserRegisterForm
from users.models import User


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Register'
        return context
