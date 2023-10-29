# Generated by Django 4.2.1 on 2023-10-29 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_city_client_city'),
        ('newsletter', '0024_newsletter_newsletter_clients_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='newsletter_cities',
            field=models.ManyToManyField(related_name='city_newsletters', to='client.city'),
        ),
    ]