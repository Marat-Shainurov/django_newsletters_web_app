from django.contrib import admin

from newsletter.models import NewsletterSettings, NewsletterAttempts, NewsletterContent


@admin.register(NewsletterSettings)
class NewsletterSettingsAdmin(admin.ModelAdmin):
    list_display = ('newsletter', 'start_campaign', 'finish_campaign', 'status', 'regularity')
    list_filter = ('newsletter', 'status')


@admin.register(NewsletterAttempts)
class NewsletterAttemptsAdmin(admin.ModelAdmin):
    list_display = ('newsletter', 'last_attempt', 'attempt_status', 'email_server_response')
    list_filter = ('newsletter', 'attempt_status', 'last_attempt')


@admin.register(NewsletterContent)
class NewsletterContentAdmin(admin.ModelAdmin):
    list_display = ('newsletter', 'newsletter_subject', 'newsletter_content')
    list_filter = ('newsletter', 'newsletter_subject')
