# Generated by Django 4.2.1 on 2023-10-30 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_alter_city_options_alter_client_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='comments',
            field=models.TextField(blank=True, null=True, verbose_name='additional_info'),
        ),
    ]
