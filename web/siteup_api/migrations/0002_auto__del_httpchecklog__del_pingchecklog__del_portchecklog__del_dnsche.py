# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'HttpCheckLog'
        db.delete_table(u'siteup_api_httpchecklog')

        # Deleting model 'PingCheckLog'
        db.delete_table(u'siteup_api_pingchecklog')

        # Deleting model 'PortCheckLog'
        db.delete_table(u'siteup_api_portchecklog')

        # Deleting model 'DnsCheckLog'
        db.delete_table(u'siteup_api_dnschecklog')

        # Adding model 'CheckLog'
        db.create_table(u'siteup_api_checklog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('status_extra', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('notified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('response_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'siteup_api', ['CheckLog'])


    def backwards(self, orm):
        # Adding model 'HttpCheckLog'
        db.create_table(u'siteup_api_httpchecklog', (
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('status_extra', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('notified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('check', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logs', to=orm['siteup_api.HttpCheck'])),
        ))
        db.send_create_signal(u'siteup_api', ['HttpCheckLog'])

        # Adding model 'PingCheckLog'
        db.create_table(u'siteup_api_pingchecklog', (
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('notified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status_extra', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('check', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logs', to=orm['siteup_api.PingCheck'])),
            ('response_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'siteup_api', ['PingCheckLog'])

        # Adding model 'PortCheckLog'
        db.create_table(u'siteup_api_portchecklog', (
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('status_extra', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('notified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('check', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logs', to=orm['siteup_api.PortCheck'])),
        ))
        db.send_create_signal(u'siteup_api', ['PortCheckLog'])

        # Adding model 'DnsCheckLog'
        db.create_table(u'siteup_api_dnschecklog', (
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('status_extra', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('notified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('check', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logs', to=orm['siteup_api.DnsCheck'])),
        ))
        db.send_create_signal(u'siteup_api', ['DnsCheckLog'])

        # Deleting model 'CheckLog'
        db.delete_table(u'siteup_api_checklog')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'siteup_api.checkgroup': {
            'Meta': {'object_name': 'CheckGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '65'})
        },
        u'siteup_api.checklog': {
            'Meta': {'object_name': 'CheckLog'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'response_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status_extra': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'siteup_api.dnscheck': {
            'Meta': {'object_name': 'DnsCheck'},
            'check_interval': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['siteup_api.CheckGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_log_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'notify_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'record_type': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '5'}),
            'resolved_address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        u'siteup_api.httpcheck': {
            'Meta': {'object_name': 'HttpCheck'},
            'check_interval': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'content_check_string': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['siteup_api.CheckGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_log_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'notify_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status_code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '200'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        u'siteup_api.pingcheck': {
            'Meta': {'object_name': 'PingCheck'},
            'check_interval': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['siteup_api.CheckGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_log_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'notify_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'should_check_timeout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timeout_value': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        u'siteup_api.portcheck': {
            'Meta': {'object_name': 'PortCheck'},
            'check_interval': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['siteup_api.CheckGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_log_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'notify_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'response_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'should_check_response': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'target_port': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        }
    }

    complete_apps = ['siteup_api']