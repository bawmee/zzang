from django.db import models
from django.db.models.fields import DateField
from datetime import datetime

# Create your models here.

class SchMst(models.Model):
    isOnWork    = models.BooleanField(default=False)
    isHome      = models.BooleanField(default=False)
    date        = models.DateTimeField(default=datetime.now())
