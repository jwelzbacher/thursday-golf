from collections import OrderedDict, defaultdict
from django.db.models import signals
from django.core.cache import cache
from django.utils import timezone
from mainframe import settings
from django.db import models
import pytz


#No models for this app, since its just for Accounts

#to set a date for an event
timezone.activate(pytz.timezone(settings.TIME_ZONE))
current_tz = timezone.get_current_timezone()
def normalise(date):
    return current_tz.normalize(date)
