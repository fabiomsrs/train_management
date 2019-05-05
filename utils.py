import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "train_management.settings")
django.setup()

import pytz
from datetime import datetime
from django.conf import settings
import functools

def get_timezone():
    return pytz.timezone(settings.TIME_ZONE_LOCAL)

def now():
    local_timezone = get_timezone()
    return datetime.now(local_timezone).replace(microsecond=0,tzinfo=None)