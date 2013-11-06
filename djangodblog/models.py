from django import get_version
from django.db import models
from django.utils.translation import ugettext_lazy as _
from distutils.version import LooseVersion

import datetime

class Error(models.Model):
    class_name = models.CharField(_('type'), max_length=128)
    path = models.TextField(max_length=512)
    message = models.TextField()
    traceback = models.TextField()
    datetime = models.DateTimeField(default=datetime.datetime.now)
    if LooseVersion(get_version()) < LooseVersion('1.5'):
        url = models.URLField(verify_exists=False, null=True, blank=True)
        referrer = models.URLField(verify_exists=False, null=True, blank=True)
    else:
        url = models.URLField(null=True, blank=True)
        referrer = models.URLField(null=True, blank=True)
    server_name = models.CharField(max_length=128, db_index=True)
    redirected = models.NullBooleanField()
    post = models.TextField()
    get = models.TextField()

    class Meta:
        verbose_name_plural = "All Errors"

class Report(models.Model):
    class Meta:
        verbose_name_plural = "Broken Link Error Report"
        managed = False #Requires Django 1.1

