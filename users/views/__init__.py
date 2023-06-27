from .register import RegisterView
from .users import user_list, UserUpdateView
from .log_in_and_out import LoginView, LogoutView
from .email_verify import verify_email
from .manager_menu import send_newsletter_manager, regular_newsletter_manager

__all__ = [
    'RegisterView', 'user_list', 'UserUpdateView', 'LoginView', 'LogoutView', 'verify_email',
    'send_newsletter_manager', 'regular_newsletter_manager',
]
