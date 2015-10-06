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
from django.contrib import admin
from facebook_api.admin import FacebookModelAdmin
from models import Page


class PageAdmin(FacebookModelAdmin):
    search_fields = ('name', 'username')
    list_display = ('name','username','category','likes_count','checkins_count','talking_about_count')
    list_filter = ('is_published',)

admin.site.register(Page, PageAdmin)
