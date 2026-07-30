from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)


def send_order_confirmation(order):
    subject = f'Order #{order.id} Confirmed - OneStep Pharmacy'
    context = {'order': order}
    html = render_to_string('emails/order_confirmation.html', context)
    text = f'Your order #{order.id} has been placed successfully. Total: Rs. {order.total}'

    _send(order.user.email, subject, text, html)


def send_shipping_update(delivery):
    subject = f'Order #{delivery.order.id} Shipping Update - OneStep Pharmacy'
    context = {'delivery': delivery, 'order': delivery.order}
    html = render_to_string('emails/shipping_update.html', context)
    text = (f'Your order #{delivery.order.id} is now: {delivery.get_status_display()}. '
            f'Tracking: {delivery.tracking_number or "N/A"}')

    _send(delivery.user.email, subject, text, html)


def send_welcome_email(user):
    subject = 'Welcome to OneStep Pharmacy!'
    context = {'user': user}
    html = render_to_string('emails/welcome.html', context)
    text = f'Welcome {user.username}! Start shopping for medicines and healthcare products.'

    _send(user.email, subject, text, html)


def send_password_reset_email(user, reset_url):
    subject = 'Reset Your Password - OneStep Pharmacy'
    context = {'user': user, 'reset_url': reset_url}
    html = render_to_string('emails/password_reset.html', context)
    text = f'Click here to reset your password: {reset_url}'

    _send(user.email, subject, text, html)


def _send(to_email, subject, text_body, html_body):
    if not to_email:
        logger.warning(f'No email address for user, skipping: {subject}')
        return
    try:
        send_mail(
            subject=subject,
            message=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            html_message=html_body,
            fail_silently=False,
        )
        logger.info(f'Email sent to {to_email}: {subject}')
    except Exception as e:
        logger.error(f'Failed to send email to {to_email}: {e}')
