from django.db import models


class Schedule(models.Model):
    mode_name = models.CharField(max_length=100, verbose_name='mode_name', unique=True)
    mode_settings = models.CharField(max_length=250, verbose_name='mode_settings')

    def __str__(self):
        return f'{self.mode_name}'

    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'