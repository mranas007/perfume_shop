from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_mail_to_client(subject, message, recipient_list, html_message=None):
    """
    Send email to client with optional HTML content
    """
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,  # Plain text version
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list,
    )

    if html_message:
        email.attach_alternative(html_message, "text/html")

    email.send()
