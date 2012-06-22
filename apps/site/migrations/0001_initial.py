# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EncryptionType'
        db.create_table('site_encryptiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('encryption_type', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('site', ['EncryptionType'])

        # Adding model 'EncryptedDisk'
        db.create_table('site_encrypteddisk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recovery_key', self.gf('django.db.models.fields.TextField')()),
            ('binary_blob', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('asset_tag', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('encryption_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.EncryptionType'])),
        ))
        db.send_create_signal('site', ['EncryptedDisk'])


    def backwards(self, orm):
        # Deleting model 'EncryptionType'
        db.delete_table('site_encryptiontype')

        # Deleting model 'EncryptedDisk'
        db.delete_table('site_encrypteddisk')


    models = {
        'site.encrypteddisk': {
            'Meta': {'object_name': 'EncryptedDisk'},
            'asset_tag': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'binary_blob': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'encryption_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['site.EncryptionType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recovery_key': ('django.db.models.fields.TextField', [], {}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'site.encryptiontype': {
            'Meta': {'object_name': 'EncryptionType'},
            'encryption_type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['site']