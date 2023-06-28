from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from users.forms import UserProfileForm
from users.models import User


@login_required
@permission_required('users.view_user', raise_exception=True)
def user_list(request):
    if request.method == 'POST':
        if 'verify_toggle' in request.POST:
            pk = request.POST.get('pk_verify_toggle')
            user = User.objects.get(pk=pk)
            user.is_verified = not user.is_verified
            user.save()
        elif 'manager_toggle' in request.POST:
            pk = request.POST.get('pk_manager_toggle')
            user = User.objects.get(pk=pk)
            user.is_manager = not user.is_manager
            user.save()
        return redirect(reverse('users:user_list'))
    else:
        all_users = User.objects.order_by('pk')
        context = {'object_list': all_users, 'page_title': 'Users list'}
        return render(request, 'users/user_list.html', context)


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:user_list')
    extra_context = {'page_title': 'Create user'}
    permission_required = 'users.add_user'


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:user_list')
    extra_context = {'page_title': 'Update users'}


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('users:user_list')
    extra_context = {'page_title': 'Delete user'}


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    extra_context = {'page_title': 'User detail'}
