# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'PostOwner', fields ['post', 'owner_content_type', 'owner_id']
        db.delete_unique('facebook_pages_postowner', ['post_id', 'owner_content_type_id', 'owner_id'])

        # Deleting model 'Post'
        db.delete_table('facebook_pages_post')

        # Deleting model 'PostOwner'
        db.delete_table('facebook_pages_postowner')

    def backwards(self, orm):
        # Adding model 'Post'
        db.create_table('facebook_pages_post', (
            ('picture', self.gf('django.db.models.fields.TextField')()),
            ('graph_id', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('object_id', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('actions', self.gf('annoying.fields.JSONField')(null=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('likes', self.gf('annoying.fields.JSONField')(null=True)),
            ('owners_json', self.gf('annoying.fields.JSONField')(null=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('author_json', self.gf('annoying.fields.JSONField')(null=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('story', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('privacy', self.gf('annoying.fields.JSONField')(null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('with_tags', self.gf('annoying.fields.JSONField')(null=True)),
            ('message_tags', self.gf('annoying.fields.JSONField')(null=True)),
            ('author_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='facebook_posts', null=True, to=orm['contenttypes.ContentType'])),
            ('comments', self.gf('annoying.fields.JSONField')(null=True)),
            ('properties', self.gf('annoying.fields.JSONField')(null=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', null=True, to=orm['facebook_applications.Application'])),
            ('comments_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('story_tags', self.gf('annoying.fields.JSONField')(null=True)),
            ('place', self.gf('annoying.fields.JSONField')(null=True)),
            ('author_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('likes_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('status_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('facebook_pages', ['Post'])

        # Adding model 'PostOwner'
        db.create_table('facebook_pages_postowner', (
            ('owner_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='facebook_page_posts', null=True, to=orm['contenttypes.ContentType'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owners', to=orm['facebook_pages.Post'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
        ))
        db.send_create_signal('facebook_pages', ['PostOwner'])

        # Adding unique constraint on 'PostOwner', fields ['post', 'owner_content_type', 'owner_id']
        db.create_unique('facebook_pages_postowner', ['post_id', 'owner_content_type_id', 'owner_id'])

    models = {
        'facebook_pages.page': {
            'Meta': {'ordering': "['name']", 'object_name': 'Page'},
            'about': ('django.db.models.fields.TextField', [], {}),
            'can_post': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'checkins': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'company_overview': ('django.db.models.fields.TextField', [], {}),
            'cover': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'graph_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '100'}),
            'location': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'picture': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'talking_about_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['facebook_pages']