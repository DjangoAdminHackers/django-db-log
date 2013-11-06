# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Error'
        db.create_table(u'djangodblog_error', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('class_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('traceback', self.gf('django.db.models.fields.TextField')()),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('referrer', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('server_name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('redirected', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'djangodblog', ['Error'])


    def backwards(self, orm):
        # Deleting model 'Error'
        db.delete_table(u'djangodblog_error')


    models = {
        u'djangodblog.error': {
            'Meta': {'object_name': 'Error'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
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