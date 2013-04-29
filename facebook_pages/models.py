# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from facebook_api import fields
from facebook_api.utils import graph
from facebook_api.models import FacebookGraphIDModel, FacebookGraphManager
import logging
import time

log = logging.getLogger('facebook_pages')

class Page(FacebookGraphIDModel):
    class Meta:
        verbose_name = 'Facebook page'
        verbose_name_plural = 'Facebook pages'
        ordering = ['name']

    name = models.CharField(max_length=200, help_text='The Page\'s name')
    link = models.URLField(max_length=100, help_text='Link to the page on Facebook')

    is_published = models.BooleanField(help_text='Indicates whether the page is published and visible to non-admins')
    can_post = models.BooleanField(help_text='Indicates whether the current session user can post on this Page')

    location = fields.JSONField(null=True, help_text='The Page\'s street address, latitude, and longitude (when available)')
    cover = fields.JSONField(null=True, help_text='The JSON object including cover_id (the ID of the photo), source (the URL for the cover photo), and offset_y (the percentage offset from top [0-100])')

    likes = models.IntegerField(null=True, help_text='The number of users who like the Page')
    checkins = models.IntegerField(null=True, help_text='The total number of users who have checked in to the Page')
    talking_about_count = models.IntegerField(null=True, help_text='The number of people that are talking about this page (last seven days)')

    category = models.CharField(max_length=100, help_text='The Page\'s category')
    phone = models.CharField(max_length=100, help_text='The phone number (not always normalized for country code) for the Page')
    picture = models.CharField(max_length=100, help_text='Link to the Page\'s profile picture') # If the "October 2012 Breaking Changes" migration setting is enabled for your app, this field will be an object with the url and is_silhouette fields; is_silhouette is true if the user has not uploaded a profile picture
    website = models.CharField(max_length=300, help_text='Link to the external website for the page')

    # for managing pages
    #access_token = models.CharField(max_length=500, help_text='A Page admin access_token for this page; The current user must be an administrator of this page; only returned if specifically requested via the fields URL parameter')

    # not in API
    username = models.CharField(max_length=200)
    company_overview = models.TextField()
    about = models.TextField()
    products = models.TextField()
    description = models.TextField()

    # auto-estimated values
    posts_count = models.IntegerField(default=0)

    objects = models.Manager()
    remote = FacebookGraphManager()

    def __unicode__(self):
        return self.name

    def parse(self, response):
        super(Page, self).parse(response)

    @property
    def wall_posts(self):
        if 'facebook_posts' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'facebook_posts' not in INSTALLED_APPS")

        from facebook_posts.models import Post
        return Post.objects.filter(graph_id__startswith='%s_' % self.graph_id) #.(owners__owner_content_type=ContentType.objects.get_for_model(Page), owners__owner_id=self.id)

    @property
    def wall_comments(self):
        if 'facebook_posts' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'facebook_posts' not in INSTALLED_APPS")

        from facebook_posts.models import Comment
        return Comment.objects.filter(graph_id__startswith='%s_' % self.graph_id)

    def fetch_posts(self, *args, **kwargs):
        '''
        Retrieve and save all posts of page
        '''
        if 'facebook_posts' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'facebook_posts' not in INSTALLED_APPS")

        from facebook_posts.models import Post
        return Post.remote.fetch_page_wall(self, *args, **kwargs)