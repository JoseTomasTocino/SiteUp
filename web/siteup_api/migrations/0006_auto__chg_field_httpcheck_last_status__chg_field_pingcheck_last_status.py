# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'HttpCheck.last_status'
        db.alter_column(u'siteup_api_httpcheck', 'last_status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['siteup_api.CheckStatus'], null=True, on_delete=models.SET_NULL))

        # Changing field 'PingCheck.last_status'
        db.alter_column(u'siteup_api_pingcheck', 'last_status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['siteup_api.CheckStatus'], null=True, on_delete=models.SET_NULL))

        # Changing field 'DnsCheck.last_status'
        db.alter_column(u'siteup_api_dnscheck', 'last_status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['siteup_api.CheckStatus'], null=True, on_delete=models.SET_NULL))

        # Changing field 'PortCheck.last_status'
        db.alter_column(u'siteup_api_portcheck', 'last_status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['siteup_api.CheckStatus'], null=True, on_delete=models.SET_NULL))

    def backwards(self, orm):

        # Changing field 'HttpCheck.last_status'
        db.alter_column(u'siteup_api_httpcheck', 'last_status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['siteup_api.CheckStatus'], null=True))

        # Changing field 'PingCheck.last_status'
        db.alter_column(u'siteup_api_pingcheck', 'last_status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['siteup_api.CheckStatus'], null=True))

        # Changing field 'DnsCheck.last_status'
        db.alter_column(u'siteup_api_dnscheck', 'last_status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['siteup_api.CheckStatus'], null=True))

        # Changing field 'PortCheck.last_status'
        db.alter_column(u'siteup_api_portcheck', 'last_status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['siteup_api.CheckStatus'], null=True))

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
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'response_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status_extra': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'siteup_api.checkstatus': {
            'Meta': {'object_name': 'CheckStatus'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status_extra': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'siteup_api.dnscheck': {
            'Meta': {'object_name': 'DnsCheck'},
            'check_interval': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['siteup_api.CheckGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_log_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['siteup_api.CheckStatus']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
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
            'last_status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['siteup_api.CheckStatus']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
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
            'last_status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['siteup_api.CheckStatus']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
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
            'last_status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['siteup_api.CheckStatus']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'notify_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'response_check_string': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'target_port': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        }
    }

    complete_apps = ['siteup_api']