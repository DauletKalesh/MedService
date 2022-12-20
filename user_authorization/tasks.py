from __future__ import absolute_import, unicode_literals

from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
import logging

logger = logging.getLogger('user_authorization.views')

@shared_task
def send_email_notification(subject, message, recipient_list):
    try:
        send_mail(subject=subject, 
                message=message, 
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list)
        return True
    except Exception as e:
        logger.warning(f"Error occured while sending message to {recipient_list}, error - {e}")
        return False
