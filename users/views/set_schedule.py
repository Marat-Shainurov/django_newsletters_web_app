from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse


def set_schedule(request):

    if request.method == 'POST':
        if 'daily' in request.POST:
            new_hour = request.POST.get('daily_hour')
            new_minute = request.POST.get('daily_minute')
            new_daily_settings = f'{new_minute} {new_hour} * * *'
            settings.REGULARITY_MODES['daily'] = new_daily_settings
        return redirect(reverse('users:set_schedule'))
    else:
        current_settings = settings.REGULARITY_MODES
        hour_list = [str(x) for x in range(9, 18)]
        minute_list = ['15', '30', '45', '0']
        dow_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dom_list = [str(x) for x in range(1, 31)]
        context = {
            'daily_settings': current_settings['daily'].split(' '),
            'weekly_settings': current_settings['weekly'].split(' '),
            'monthly_settings': current_settings['monthly'].split(' '),
            'minute_list': minute_list,
            'hour_list': hour_list,
            'dow_list': dow_list,
            'dom_list': dom_list,
            'page_title': 'Schedule settings'
        }
    return render(request, 'users/set_schedule.html', context)
