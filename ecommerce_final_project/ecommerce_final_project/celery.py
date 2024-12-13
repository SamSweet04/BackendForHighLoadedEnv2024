from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_final_project.settings')

# Create an instance of the Celery class and configure it.
app = Celery('ecommerce_final_project')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks.py in all Django apps.
app.autodiscover_tasks()
