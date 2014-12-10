# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Page.likes'
        db.delete_column(u'facebook_pages_page', 'likes')

        # Deleting field 'Page.checkins'
        db.delete_column(u'facebook_pages_page', 'checkins')

        # Adding field 'Page.likes_count'
        db.add_column(u'facebook_pages_page', 'likes_count',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Page.checkins_count'
        db.add_column(u'facebook_pages_page', 'checkins_count',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Page.likes'
        db.add_column(u'facebook_pages_page', 'likes',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Page.checkins'
        db.add_column(u'facebook_pages_page', 'checkins',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Deleting field 'Page.likes_count'
        db.delete_column(u'facebook_pages_page', 'likes_count')

        # Deleting field 'Page.checkins_count'
        db.delete_column(u'facebook_pages_page', 'checkins_count')


    models = {
        u'facebook_pages.page': {
            'Meta': {'object_name': 'Page'},
            'about': ('django.db.models.fields.TextField', [], {}),
            'can_post': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'checkins_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'company_overview': ('django.db.models.fields.TextField', [], {}),
            'cover': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'graph_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'location': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'picture': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'posts_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'products': ('django.db.models.fields.TextField', [], {}),
            'talking_about_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['facebook_pages']