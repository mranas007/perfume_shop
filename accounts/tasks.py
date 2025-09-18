from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

logger = get_task_logger(__name__)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    name='accounts.send_mail_to_client',
    autoretry_for=(Exception,),
    retry_backoff=True
)
def send_mail_to_client(self, subject, message, recipient_list, html_message=None):
    """
    Send email to client with optional HTML content
    
    Args:
        subject (str): Email subject
        message (str): Plain text message
        recipient_list (str|list): Single email or list of emails
        html_message (str, optional): HTML version of the message
    """
    try:
        # Ensure recipient_list is a list
        recipients = [recipient_list] if isinstance(recipient_list, str) else recipient_list
        
        logger.info(f"Sending email to {recipients}")
        
        # Create email message
        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients
        )

        if html_message:
            email.attach_alternative(html_message, "text/html")

        # Send email
        email.send(fail_silently=False)
        logger.info(f"Email sent successfully to {recipients}")

    except Exception as exc:
        logger.error(f"Failed to send email to {recipients}: {str(exc)}")
        raise self.retry(exc=exc)
