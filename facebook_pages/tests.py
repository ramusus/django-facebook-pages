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
from bs4 import BeautifulSoup
from facebook_api.utils import get_or_create_from_small_resource
from facebook_api.tests import FacebookApiTestCase

from .factories import PageFactory
from .models import Page, PAGES_FANS_USER_ID
from .parser import FacebookPageFansParser

PAGE_ID = '19292868552'
PAGE_RESOURCE_SHORT = {'category': 'Product/service', 'id': PAGE_ID, 'name': 'Facebook Developers'}
PAGE_URL = 'https://www.facebook.com/pages/METRO-Cash-and-Carry-Russia/129107667156177'
PAGE_FANS_ID = 501842786534856


class FacebookPagesTest(FacebookApiTestCase):

    def test_get_by_slug(self):

        slugs = [
            'pages/METRO-Cash-and-Carry-Russia/129107667156177',
            'tinkoff.ins/',
        ]
        for slug in slugs:
            page = Page.remote.get_by_slug(slug)
            self.assertIsInstance(page, Page)

        self.assertEqual(Page.objects.count(), 0)

    def test_fetch_page(self):

        self.assertEqual(Page.objects.count(), 0)
        page = Page.remote.fetch(PAGE_ID)
        page = Page.remote.fetch(PAGE_ID)
        self.assertEqual(Page.objects.count(), 1)

        self.assertEqual(page.graph_id, PAGE_ID)
        self.assertEqual(page.name, 'Facebook Developers')
        self.assertEqual(page.is_published, True)
        self.assertEqual(page.website, 'http://developers.facebook.com')
        self.assertEqual(page.category, "Product/service")
        self.assertEqual(page.username, 'FacebookDevelopers')
        self.assertEqual(page.link, 'https://www.facebook.com/FacebookDevelopers')
        self.assertGreater(len(page.company_overview), 0)
        self.assertGreater(page.likes_count, 0)

        page.username = page.website = ''
        self.assertEqual(page.username, '')
        self.assertEqual(page.website, '')
        page.save()
        page = Page.remote.fetch(PAGE_ID)
        self.assertEqual(page.username, 'FacebookDevelopers')
        self.assertEqual(page.website, 'http://developers.facebook.com')

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


class FacebookPageFansTest(FacebookApiTestCase):

    def test_get_parser_response(self):

        parser = FacebookPageFansParser(
            authorized=True, url='/ajax/browser/list/page_fans/?page_id=%s&start=0&__user=%s&__a=1' % (PAGE_FANS_ID, PAGES_FANS_USER_ID))
        self.assertIsInstance(parser.content_bs, BeautifulSoup)

    def test_fetch_fans_ids(self):

        page = PageFactory(graph_id=PAGE_FANS_ID)

        ids = page.fetch_fans_ids_parser()
        self.assertGreater(len(ids), 450)
