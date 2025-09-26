from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from orders.models import Order


@shared_task(
    bind=True,
    max_retries=2,
    default_retry_delay=60,
    name='cart.send_mail_to_owner',
    autoretry_for=(Exception,),
    retry_backoff=True
)
def send_mail_to_owner(self, order_id, order_items, total_amount, message=None):
    """
        Send order notification email to the shop owner.
    """
    try:
        order = Order.objects.get(id=order_id)  # Fetch order here

        subject = f"New Order Placed: #{order.id}"
        recipients = ["adnanperfume84@gmail.com"]
        html_message = render_to_string(
            'cart/email/owner_order_email.html',
            {'order': order, 'order_items': order_items, 'total_amount': total_amount}
        )

        email = EmailMultiAlternatives(
            subject=subject,
            body=message or "",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients,
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)

    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task(
    bind=True,
    max_retries=2,
    default_retry_delay=60,
    name='cart.send_mail_to_client',
    autoretry_for=(Exception,),
    retry_backoff=True
)
def send_mail_to_client(self, order_id, order_items, total_amount, user_email, message=None):
    """
        Send order confirmation email to the client.
    """
    try:
        order = Order.objects.get(id=order_id)  # Fetch order here

        subject = f"Order Confirmation #{order.id}"
        recipients = user_email if isinstance(user_email, list) else [user_email]
        html_message = render_to_string(
            'cart/email/client_order_email.html',
            {'order': order, 'order_items': order_items, 'total_amount': total_amount}
        )

        email = EmailMultiAlternatives(
            subject=subject,
            body=message or "",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients,
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)

    except Exception as exc:
        raise self.retry(exc=exc)
