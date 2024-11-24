import logging
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver

security_logger = logging.getLogger('security')

@receiver(user_logged_in)
def log_successful_login(sender, request, user, **kwargs):
    security_logger.info(f"Successful login by user: {user.username} from IP: {request.META.get('REMOTE_ADDR')}")

@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    security_logger.warning(f"Failed login attempt for user: {credentials.get('username')} from IP: {request.META.get('REMOTE_ADDR')}")
