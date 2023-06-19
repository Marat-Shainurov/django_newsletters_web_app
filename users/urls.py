from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, verify_email, UserListView,UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegisterView.as_view(), name='register'),
    path('registration/verification/<str:email>', verify_email, name='verify_email'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('list/update/<int:pk>', UserUpdateView.as_view(), name='user_form'),
]
