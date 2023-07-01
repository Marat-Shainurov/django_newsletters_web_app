from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.urls import reverse

from newsletter.models import Schedule, Newsletter
from users.services import get_wod_setting

@login_required
@permission_required('users.set_schedule', raise_exception=True)
def set_schedule(request):

    if request.method == 'POST':
        if 'daily' in request.POST:
            new_hour = request.POST.get('daily_hour')
            new_minute = request.POST.get('daily_minute')
            new_daily_settings = f'{new_minute} {new_hour} * * *'
            daily_mode = Schedule.objects.get(mode_name='daily')
            daily_mode.mode_settings = new_daily_settings
            daily_mode.save()
        if 'weekly' in request.POST:
            new_hour = request.POST.get('weekly_hour')
            new_minute = request.POST.get('weekly_minute')
            new_day = request.POST.get('weekly_day')
            new_weekly_settings = f'{new_minute} {new_hour} * * {get_wod_setting(new_day)}'
            weekly_mode = Schedule.objects.get(mode_name='weekly')
            weekly_mode.mode_settings = new_weekly_settings
            weekly_mode.save()
        if 'monthly' in request.POST:
            new_hour = request.POST.get('monthly_hour')
            new_minute = request.POST.get('monthly_minute')
            new_day = request.POST.get('monthly_day')
            new_monthly_settings = f'{new_minute} {new_hour} {new_day} * *'
            monthly_mode = Schedule.objects.get(mode_name='monthly')
            monthly_mode.mode_settings = new_monthly_settings
            monthly_mode.save()

        return redirect(reverse('users:set_schedule'))

    else:
        all_schedules = Schedule.objects.all()
        hour_list = [str(x) for x in range(9, 19)]
        minute_list = ['15', '30', '45', '0']
        dow_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dom_list = [str(x) for x in range(1, 32)]

        context = {
            'daily_settings': Schedule.objects.get(mode_name='daily'),
            'weekly_settings': Schedule.objects.get(mode_name='weekly'),
            'monthly_settings': Schedule.objects.get(mode_name='monthly'),
            'all_schedules': all_schedules,
            'minute_list': minute_list,
            'hour_list': hour_list,
            'dow_list': dow_list,
            'dom_list': dom_list,
            'page_title': 'Schedule settings'
        }

    return render(request, 'users/set_schedule.html', context)
