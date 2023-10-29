from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from client.models import Client
from newsletter.models import Newsletter
from users.forms import UserProfileForm
from users.models import User
from users.services import get_cached_users_for_list_table


@login_required
def user_list(request):
    context = {'object_list': get_cached_users_for_list_table(), 'page_title': 'Users list'}
    return render(request, 'users/user_list.html', context)


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:user_list')
    extra_context = {'page_title': 'Create user'}
    permission_required = 'users.add_user'


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserProfileForm
    extra_context = {'page_title': 'Update users'}
    permission_required = 'users.change_user'

    def get_success_url(self):
        return reverse('users:user_detail', kwargs={'pk': self.object.pk})


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('users:user_list')
    extra_context = {'page_title': 'Delete user'}
    permission_required = 'users.delete_user'


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    extra_context = {'page_title': 'User detail'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = kwargs.get('object')
        context['user_clients'] = Client.objects.filter(user=user).count()
        context['newsletter_user'] = Newsletter.objects.filter(newsletter_user=user).count()
        return context

    def post(self, *args, **kwargs):

        if 'verify_toggle' in self.request.POST:
            pk = self.request.POST.get('pk_verify_toggle')
            user = User.objects.get(pk=pk)
            user.is_verified = not user.is_verified
            user.save()

        return redirect('users:user_detail', pk=self.kwargs['pk'])
