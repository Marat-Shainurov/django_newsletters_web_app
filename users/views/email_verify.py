from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse

from users.models import User


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
        context = {'page_title': 'Email verification'}
        return render(request, 'users/verify_email.html', context)
