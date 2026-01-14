from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 10})
def send_email_task(self, subject, username, recipient):
    html_content = render_to_string(
        "emails/welcome_email.html",
        {"username": username}
    )

    text_content = f"Hi {username}, Thanks for registering on our blog!"

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [recipient]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
