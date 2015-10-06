# -*- coding: utf-8 -*-
'''
Copyright 2011-2015 ramusus
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import logging
import re

from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from facebook_api import fields
from facebook_api.decorators import atomic
from facebook_api.models import FacebookGraphIDModel, FacebookGraphManager
from facebook_api.utils import get_improperly_configured_field

from .parser import FacebookPageFansParser, FacebookParseError

if 'facebook_photos' in settings.INSTALLED_APPS:
    from facebook_photos.models import Album
    albums = get_improperly_configured_field('facebook_photos', True)
    # albums = generic.GenericRelation(
    #     Album, content_type_field='author_content_type', object_id_field='author_id', verbose_name=u'Albums')

    def fetch_albums(self, *args, **kwargs):
        return Album.remote.fetch_page(page=self, *args, **kwargs)
else:
    albums = get_improperly_configured_field('facebook_photos', True)
    fetch_albums = get_improperly_configured_field('facebook_photos')

log = logging.getLogger('facebook_pages')

PAGES_FANS_USER_ID = getattr(settings, 'FACEBOOK_PAGES_FANS_USER_ID', '')


class FacebookPageGraphManager(FacebookGraphManager):

    def get_by_slug(self, slug):
        '''
        Return object by slug
        '''
        # no slug pages - https://www.facebook.com/pages/METRO-Cash-and-Carry-Russia/129107667156177
        if slug[:5] == 'pages':
            m = re.findall(r'^pages/.+/(\d+)', slug)
            slug = m[0]
        return self.fetch(slug)


class Page(FacebookGraphIDModel):

    name = models.CharField(max_length=200, help_text='The Page\'s name')
    link = models.URLField(max_length=1000, help_text='Link to the page on Facebook')

    is_published = models.BooleanField(
        help_text='Indicates whether the page is published and visible to non-admins', default=False)
    can_post = models.BooleanField(
        help_text='Indicates whether the current session user can post on this Page', default=False)

    location = fields.JSONField(
        null=True, help_text='The Page\'s street address, latitude, and longitude (when available)')
    cover = fields.JSONField(
        null=True, help_text='The JSON object including cover_id (the ID of the photo), source (the URL for the cover photo), and offset_y (the percentage offset from top [0-100])')

    likes_count = models.IntegerField(null=True, help_text='The number of users who like the Page')
    checkins_count = models.IntegerField(
        null=True, help_text='The total number of users who have checked in to the Page')
    talking_about_count = models.IntegerField(
        null=True, help_text='The number of people that are talking about this page (last seven days)')

    category = models.CharField(max_length=100, help_text='The Page\'s category')
    phone = models.TextField(help_text='The phone number (not always normalized for country code) for the Page')
    # If the "October 2012 Breaking Changes" migration setting is enabled for
    # your app, this field will be an object with the url and is_silhouette
    # fields; is_silhouette is true if the user has not uploaded a profile
    # picture
    picture = models.CharField(max_length=100, help_text='Link to the Page\'s profile picture')
    website = models.CharField(max_length=1000, help_text='Link to the external website for the page')

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

    albums = albums
    fetch_albums = fetch_albums

    objects = models.Manager()
    remote = FacebookPageGraphManager()

    class Meta:
        verbose_name = 'Facebook page'
        verbose_name_plural = 'Facebook pages'

    def __unicode__(self):
        return self.name

    def parse(self, response):

        for field_name in ['likes', 'checkins']:
            response['%s_count' % field_name] = response.get(field_name)

        super(Page, self).parse(response)

    @property
    def slug(self):
        return self.username or self.graph_id

    @property
    def wall_posts(self):
        if 'facebook_posts' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'facebook_posts' not in INSTALLED_APPS")

        from facebook_posts.models import Post
        # .(owners__owner_content_type=ContentType.objects.get_for_model(Page), owners__owner_id=self.id)
        return Post.objects.filter(graph_id__startswith='%s_' % self.graph_id)

    @property
    def wall_comments(self):
        if 'facebook_posts' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'facebook_posts' not in INSTALLED_APPS")

        from facebook_posts.models import Comment
        return Comment.objects.filter(graph_id__startswith='%s_' % self.graph_id)

    @atomic
    def fetch_posts(self, *args, **kwargs):
        '''
        Retrieve and save all posts of page
        '''
        if 'facebook_posts' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'facebook_posts' not in INSTALLED_APPS")

        from facebook_posts.models import Post
        return Post.remote.fetch_page(page=self, *args, **kwargs)

#    @atomic
    def fetch_fans(self, *args, **kwargs):
        return self.fetch_fans_ids_parser()

    def fetch_fans_ids_parser(self):
        ids = []
        offset = 0
        parser = FacebookPageFansParser()
        while True:
            try:
                users = self.parse_fans(parser, offset)
                assert len(users) > 0
            except (FacebookParseError, AssertionError):
                break

            ids += [user.graph_id for user in users]
            offset += 10

#            print offset, len(ids)

        return ids

    def parse_fans(self, parser, offset=0):

        if 'facebook_users' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'facebook_users' not in INSTALLED_APPS")
        from facebook_users.models import User

        parser.request(authorized=True, url='/ajax/browser/list/page_fans/?page_id=%s&start=%s&__user=%s&__a=1' %
                       (self.graph_id, offset, PAGES_FANS_USER_ID))

        users = []
        for item in parser.content_bs.findAll('li', {'class': 'adminableItem fbProfileBrowserListItem'}):
            initial = {'graph_id': item['id'].replace('adminableItem_', '')}
            name = item.find('div', {'class': 'uiProfileBlockContent'}).find('a').text

            # https://www.facebook.com/milkamelot?fref=pb
            href = item.find('a')['href']
            if 'profile.php' in href:
                initial['username'] = href.split('?')[0].split('/')[3]

            user = User(**initial)
            user.set_name(name)
            users += [user]

        return users
