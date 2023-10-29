from django.contrib import admin

from newsletter.models import Newsletter, NewsletterAttempts, EmailServerResponse, Schedule


@admin.register(Newsletter)
class NewsletterSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'newsletter', 'start_campaign', 'finish_campaign', 'status', 'regularity', 'subject', 'is_active',
        'created')
    list_filter = ('newsletter', 'status')


@admin.register(NewsletterAttempts)
class NewsletterAttemptsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'newsletter', 'last_attempt', 'attempt_status')
    list_filter = ('newsletter', 'attempt_status', 'last_attempt')


@admin.register(EmailServerResponse)
class EmailServerResponseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'attempt', 'recipient_email', 'response')
    list_filter = ('attempt', 'recipient_email')


@admin.register(Schedule)
class EmailServerResponseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mode_name', 'mode_settings')
