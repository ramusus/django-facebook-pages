# -*- coding: utf-8 -*-
from django.contrib import admin
from facebook_api.admin import FacebookModelAdmin
from models import Page

class PageAdmin(FacebookModelAdmin):
    list_display = ('name','username','category','likes','checkins','talking_about_count')
    list_filter = ('is_published',)

admin.site.register(Page, PageAdmin)