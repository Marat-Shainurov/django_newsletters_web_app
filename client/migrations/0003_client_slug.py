# Generated by Django 4.2.1 on 2023-06-06 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_client_email_alter_client_is_signed_up_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name='slug'),
        ),
    ]
