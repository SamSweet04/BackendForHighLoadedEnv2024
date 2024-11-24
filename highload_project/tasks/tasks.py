import logging
from celery import shared_task
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_email_task(self, recipient, subject, body):
    try:
        logger.info(f"Attempting to send email to {recipient}")
        send_mail(subject, body, 'saule.arystanbek.2004@mail.ru', [recipient])
        logger.info(f"Email sent to {recipient}")
        return f"Email sent to {recipient}"
    except Exception as exc:
        logger.error(f"Failed to send email to {recipient}, retrying. Error: {exc}")
        raise self.retry(exc=exc, countdown=60)
