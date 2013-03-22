# -*- coding: utf-8 -*-
from django.test import TestCase
from models import Page
from facebook_posts.models import Post, get_or_create_from_small_resource

PAGE_ID = '19292868552'
PAGE_RESOURCE_SHORT = {'category': 'Product/service', 'id': PAGE_ID, 'name': 'Facebook Developers'}

class FacebookPagesTest(TestCase):

    def test_fetch_page(self):

        self.assertEqual(Page.objects.count(), 0)
        Page.remote.fetch(PAGE_ID)
        Page.remote.fetch(PAGE_ID)
        self.assertEqual(Page.objects.count(), 1)

        page = Page.remote.all()[0]
        self.assertEqual(page.graph_id, PAGE_ID)
        self.assertEqual(page.name, 'Facebook Developers')
        self.assertEqual(page.is_published, True)
        self.assertEqual(page.website, 'http://developers.facebook.com')
        self.assertEqual(page.category, "Product/service")
        self.assertEqual(page.username, 'FacebookDevelopers')
        self.assertEqual(page.company_overview, 'Facebook Platform enables anyone to build social apps on Facebook, mobile, and the web.')
        self.assertEqual(page.about, 'Build and distribute amazing social apps on Facebook. https://developers.facebook.com/')
        self.assertEqual(page.link, 'http://www.facebook.com/FacebookDevelopers')

    def test_fetch_posts_of_page(self):

        Page.remote.fetch(PAGE_ID)

        page = Page.objects.all()[0]

        self.assertEqual(Post.objects.count(), 0)
        page.fetch_posts()
        self.assertTrue(Post.objects.count() > 10)

    def test_fetch_page_from_resource(self):

        Page.remote.fetch(PAGE_ID)

        page = get_or_create_from_small_resource(PAGE_RESOURCE_SHORT)
        self.assertEqual(page.name, PAGE_RESOURCE_SHORT['name'])
        self.assertEqual(page.category, PAGE_RESOURCE_SHORT['category'])

        page1 = Page.objects.all()[0]
        self.assertEqual(page1.website, "http://developers.facebook.com")

        page2 = get_or_create_from_small_resource(PAGE_RESOURCE_SHORT)
        self.assertEqual(page2.website, "http://developers.facebook.com")
        self.assertEqual(page2.category, PAGE_RESOURCE_SHORT['category'])