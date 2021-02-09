from django.contrib.auth.models import AbstractUser # To create a custom user model
from django.core.validators import MaxValueValidator, MinValueValidator # To set minimum and maximum integer valuses
from django.conf import settings
from datetime import datetime, time, date
from django.utils import timezone
from django.db import models