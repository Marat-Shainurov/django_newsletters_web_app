from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, verify_email, UserListView, UserUpdateView, login_warning, \
    send_newsletter_manager, launch_regular_manager, remove_regular_manager

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegisterView.as_view(), name='register'),
    path('registration/verification/<str:email>', verify_email, name='verify_email'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('list/update/<int:pk>', UserUpdateView.as_view(), name='user_form'),
    path('login/warning/', login_warning, name='login_warning'),
    path('manager/send-newsletter/', send_newsletter_manager, name='send_newsletter_manager'),
    path('manager/launch-regular-newsletter/', launch_regular_manager, name='launch_regular_manager'),
    path('manager/remove-regular-manager/', remove_regular_manager, name='remove_regular_manager')
]
