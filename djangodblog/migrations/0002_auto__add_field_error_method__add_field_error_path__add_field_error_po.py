# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Error.method'
        db.add_column(u'djangodblog_error', 'method',
                      self.gf('django.db.models.fields.CharField')(default='GET', max_length=32),
                      keep_default=False)

        # Adding field 'Error.path'
        db.add_column(u'djangodblog_error', 'path',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=512),
                      keep_default=False)

        # Adding field 'Error.post'
        db.add_column(u'djangodblog_error', 'post',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Error.get'
        db.add_column(u'djangodblog_error', 'get',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Error.cookies'
        db.add_column(u'djangodblog_error', 'cookies',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Error.method'
        db.delete_column(u'djangodblog_error', 'method')

        # Deleting field 'Error.path'
        db.delete_column(u'djangodblog_error', 'path')

        # Deleting field 'Error.post'
        db.delete_column(u'djangodblog_error', 'post')

        # Deleting field 'Error.get'
        db.delete_column(u'djangodblog_error', 'get')

        # Deleting field 'Error.cookies'
        db.delete_column(u'djangodblog_error', 'cookies')


    models = {
        u'djangodblog.error': {
            'Meta': {'object_name': 'Error'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'cookies': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'get': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'method': ('django.db.models.fields.CharField', [], {'default': "'GET'", 'max_length': '32'}),
            'path': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '512'}),
            'post': ('django.db.models.fields.TextField', [], {'default': "''"}),
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