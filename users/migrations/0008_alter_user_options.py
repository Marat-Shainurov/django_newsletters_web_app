# Generated by Django 4.2.1 on 2023-07-01 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('block_user', 'can block users'), ('set_schedule', 'can set schedule')], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
