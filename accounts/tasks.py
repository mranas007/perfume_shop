from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


@shared_task
def send_mail_to_client(subject, message, recipient_list, html_message=None):
    """
    Send email to client with optional HTML content
    """
    from_email_address = getattr(settings, 'DEFAULT_FROM_EMAIL')
    from_name = getattr(settings, 'DEFAULT_FROM_NAME', '') # Provide a fallback
    
    # Construct the formatted "From" string
    from_header = f'"{from_name}" <{from_email_address}>' if from_name else from_email_address

    email = EmailMultiAlternatives(
        subject=subject,
        body=message,  # Plain text version
        from_email=from_header, # <-- Use the new formatted from_header
        to=recipient_list,
    )

    if html_message:
        email.attach_alternative(html_message, "text/html")

    email.send()
