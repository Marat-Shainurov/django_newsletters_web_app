from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, verify_email, UserUpdateView, user_list, UserCreateView, \
    UserDetailView, UserDeleteView

app_name = UsersConfig.name

urlpatterns = [
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/logout/', LogoutView.as_view(), name='logout'),
    path('users/registration/', RegisterView.as_view(), name='register'),
    path('users/registration/verification/<str:email>', verify_email, name='verify_email'),
    path('users/manager/list/', user_list, name='user_list'),
    path('users/manager/create-user/', UserCreateView.as_view(), name='user_form'),
    path('users/manager/user-detail/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('users/manager/user-delete/<int:pk>', UserDeleteView.as_view(), name='user_delete'),
    path('users/manager/update/<int:pk>', UserUpdateView.as_view(), name='user_form')
]
