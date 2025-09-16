from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


@shared_task
def send_mail_to_client(subject, message, recipient_list, html_message=None):
    """
    Send email to client with optional HTML content
    """
    # Use verified sender or Resend's default for testing
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')

    email = EmailMultiAlternatives(
        subject=subject,
        body=message,  # Plain text version
        from_email=from_email,
        to=recipient_list,
    )

    if html_message:
        email.attach_alternative(html_message, "text/html")

    email.send()
