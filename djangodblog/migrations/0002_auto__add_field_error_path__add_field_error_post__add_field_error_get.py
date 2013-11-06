# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Error.path'
        db.add_column(u'djangodblog_error', 'path',
                      self.gf('django.db.models.fields.TextField')(default=None, max_length=512),
                      keep_default=False)

        # Adding field 'Error.post'
        db.add_column(u'djangodblog_error', 'post',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Error.get'
        db.add_column(u'djangodblog_error', 'get',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Error.path'
        db.delete_column(u'djangodblog_error', 'path')

        # Deleting field 'Error.post'
        db.delete_column(u'djangodblog_error', 'post')

        # Deleting field 'Error.get'
        db.delete_column(u'djangodblog_error', 'get')


    models = {
        u'djangodblog.error': {
            'Meta': {'object_name': 'Error'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'get': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'path': ('django.db.models.fields.TextField', [], {'max_length': '512'}),
            'post': ('django.db.models.fields.TextField', [], {}),
            'redirected': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'referrer': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'server_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'traceback': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'djangodblog.report': {
            'Meta': {'object_name': 'Report', 'managed': 'False'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['djangodblog']