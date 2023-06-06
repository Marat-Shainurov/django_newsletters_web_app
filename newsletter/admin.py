from django.contrib import admin

from newsletter.models import Newsletter, NewsletterAttempts


@admin.register(Newsletter)
class NewsletterSettingsAdmin(admin.ModelAdmin):
    list_display = (
    'pk', 'newsletter', 'start_campaign', 'finish_campaign', 'status', 'regularity', 'subject', 'is_active', 'created')
    list_filter = ('newsletter', 'status')


@admin.register(NewsletterAttempts)
class NewsletterAttemptsAdmin(admin.ModelAdmin):
    list_display = ('newsletter', 'last_attempt', 'attempt_status', 'email_server_response')
    list_filter = ('newsletter', 'attempt_status', 'last_attempt')
