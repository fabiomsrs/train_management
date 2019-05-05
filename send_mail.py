import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "train_management.settings")
django.setup()

from django.core.mail import send_mail
from train_management.settings import EMAIL_HOST_USER
send_mail(
    'Teste',
    'Ta funcionando.',
    EMAIL_HOST_USER,
    ['matmthe@gmail.com'],
    fail_silently=False,
)