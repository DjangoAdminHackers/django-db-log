from django import get_version
from django.db import models
from django.utils.translation import ugettext_lazy as _
from distutils.version import LooseVersion
from django.template.loader import render_to_string
import base64
import json
import datetime

class Error(models.Model):
    method = models.CharField(max_length=32, default='GET')
    path = models.TextField(max_length=512, default='')
    class_name = models.CharField(_('type'), max_length=128)
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
    post = models.TextField(default='')
    get = models.TextField(default='')
    cookies = models.TextField(default='')

    @property
    def portable_request(self):
        return render_to_string('admin/portable.html', {
            'string': base64.b64encode(json.dumps({
                'method': self.method,
                'path': self.path,
                'get': json.loads(self.get),
                'post':json.loads(self.post),
                'cookies': json.loads(self.cookies),
            }))
        })
    class Meta:
        verbose_name_plural = "All Errors"

class Report(models.Model):
    class Meta:
        verbose_name_plural = "Broken Link Error Report"
        managed = False #Requires Django 1.1

