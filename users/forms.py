from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError

from newsletter.models import Newsletter
from users.models import User


class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_verified:
            raise ValidationError('Your user is blocked! Please contact your manager.')
        else:
            super().confirm_login_allowed(user)


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'avatar', 'is_verified', 'is_manager')
