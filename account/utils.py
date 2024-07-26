from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from .tokens import account_activation_token
from general.utils import get_logger

logger = get_logger('file')

def user_is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def send_verification_email(user):
    mail_subject = 'Verifikasi Email'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    message = render_to_string('acc_email_verification.html', {
        'user': user,
        'verify_url': f'{settings.FRONTEND_URL}/{uid}/{token}',
    })

    try:
        send_mail(
            mail_subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
            html_message=message
        )

    except Exception as e:
        logger.error(f'Failed to send verification email to {user.email}: {e}')