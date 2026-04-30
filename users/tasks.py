from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist

from users.generate_token import account_activation_token

User = get_user_model()


@shared_task
def send_simple_email(subject, body, email):
    """
    Standard task to send a basic text email.
    """
    send_mail(
        subject=subject,
        message=body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )


@shared_task
def registration_mail_task(subject, user_id, domain):
    """
    Background task to send the activation email.
    Note: Always pass simple data (like strings/IDs) to Celery tasks.
    """
    try:
        user = User.objects.get(pk=user_id)
        token = account_activation_token.make_token(user)

        # Using 'user' instead of 'users' in context for consistency with views
        context = {
            "user": user,
            "domain": domain,
            "token": token,
            "user_pk": user.pk
        }

        message = render_to_string("users/authentication.html", context)

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email]
        )
        email.send(fail_silently=False)

    except ObjectDoesNotExist:
        # Log error or handle cases where user was deleted before task started
        pass