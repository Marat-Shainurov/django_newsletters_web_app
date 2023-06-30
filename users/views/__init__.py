from .register import RegisterView
from .users import user_list, UserUpdateView, UserCreateView, UserDeleteView, UserDetailView
from .log_in_and_out import LoginView, LogoutView
from .email_verify import verify_email


__all__ = [
    'RegisterView', 'user_list', 'UserUpdateView', 'LoginView', 'LogoutView', 'verify_email',
    'UserCreateView', 'UserDeleteView', 'UserDetailView'
]
