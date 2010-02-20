from django.db import models
from django.utils.translation import ugettext_lazy as _

import datetime

class Error(models.Model):
    class_name      = models.CharField(_('type'), max_length=128)
    message         = models.TextField()
    traceback       = models.TextField()
    datetime        = models.DateTimeField(default=datetime.datetime.now)
    url             = models.URLField(verify_exists=False, null=True, blank=True)
    referrer        = models.URLField(verify_exists=False, null=True, blank=True)
    server_name     = models.CharField(max_length=128, db_index=True)
    redirected      = models.NullBooleanField()

class Report(models.Model):
    class Meta:
        managed = False #Requires Django 1.1

