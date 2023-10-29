from datetime import datetime
from smtplib import SMTPException

from dateutil.tz import tz
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.core.validators import EmailValidator, ValidationError

from newsletter.models import Newsletter, NewsletterAttempts, EmailServerResponse


def send_newsletter(newsletter_id):
    """
    Sends emails to each signed up client of the selected cities.
    Depending on the sending results the new_attempt.attempt_status (sending attempt's status)
    and new_response_obj.response (each email's server response) values are assigned.
    """
    newsletter_to_send = Newsletter.objects.get(pk=newsletter_id)
    request_user = newsletter_to_send.newsletter_user
    newsletter_cities = newsletter_to_send.newsletter_cities
    recipients_list = []

    for city in newsletter_cities:
        city_clients = city.city_clients.filter(is_signed_up=True, user=request_user)
        city_recipients = [x.email for x in city_clients]
        recipients_list.append(city_recipients)

    timezone = tz.gettz(settings.TIME_ZONE)
    actual_time = datetime.now(timezone)

    new_attempt = NewsletterAttempts.objects.create(newsletter=newsletter_to_send, last_attempt=actual_time)
    email_validator = EmailValidator()

    if len(recipients_list) == 0:
        new_attempt.attempt_status = 'failure'
        new_attempt.comment = 'No emails to inform'
        new_attempt.save()

    informed_clients_count = 0

    for address in recipients_list:
        new_response_obj = EmailServerResponse.objects.create(attempt=new_attempt, recipient_email=address)

        try:
            email_validator(address)
            send_mail(
                f'{newsletter_to_send.subject}',
                f'{newsletter_to_send.content}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[address],
            )
        except (SMTPException, BadHeaderError, ValidationError) as error:
            new_response_obj.response = str(error)
        except Exception as e:
            new_response_obj.response = str(e)
        else:
            new_response_obj.response = 'Successful sending.'
            informed_clients_count += 1
        finally:
            new_response_obj.save()

    new_attempt.attempt_status = 'success'
    new_attempt.comment = f'{informed_clients_count} clients have been informed out of {len(recipients_list)}'
    new_attempt.save()
