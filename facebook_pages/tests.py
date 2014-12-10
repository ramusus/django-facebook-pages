# -*- coding: utf-8 -*-
from django.test import TestCase
from models import Page
from facebook_posts.models import Post, get_or_create_from_small_resource

PAGE_ID = '19292868552'
PAGE_RESOURCE_SHORT = {'category': 'Product/service', 'id': PAGE_ID, 'name': 'Facebook Developers'}
PAGE_URL = 'https://www.facebook.com/pages/METRO-Cash-and-Carry-Russia/129107667156177'

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
        self.assertEqual(page.link, 'http://www.facebook.com/FacebookDevelopers')

    def test_get_by_url(self):

        page = Page.remote.get_by_url('https://www.facebook.com/pages/METRO-Cash-and-Carry-Russia/129107667156177')

        self.assertEqual(page.graph_id, '129107667156177')
        self.assertEqual(page.name, 'METRO Cash and Carry Russia')
        self.assertEqual(page.is_published, True)
        self.assertEqual(page.website, 'http://www.metro-cc.ru')

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