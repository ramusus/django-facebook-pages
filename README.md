Django Facebook Graph API Ads
=============================

[![PyPI version](https://badge.fury.io/py/django-facebook-ads.png)](http://badge.fury.io/py/django-facebook-ads) [![Build Status](https://travis-ci.org/ramusus/django-facebook-pages.png?branch=master)](https://travis-ci.org/ramusus/django-facebook-pages) [![Coverage Status](https://coveralls.io/repos/ramusus/django-facebook-pages/badge.png?branch=master)](https://coveralls.io/r/ramusus/django-facebook-pages)

Application for interacting with Facebook Graph API Pages objects using Django model interface

Installation
------------

    pip install django-facebook-pages

Add into `settings.py` lines:

    INSTALLED_APPS = (
        ...
        'oauth_tokens',
        'facebook_api',
        'facebook_ads',
    )

    # oauth-tokens settings
    OAUTH_TOKENS_HISTORY = True                                        # to keep in DB expired access tokens
    OAUTH_TOKENS_FACEBOOK_CLIENT_ID = ''                               # application ID
    OAUTH_TOKENS_FACEBOOK_CLIENT_SECRET = ''                           # application secret key
    OAUTH_TOKENS_FACEBOOK_SCOPE = ['offline_access']                   # application scopes
    OAUTH_TOKENS_FACEBOOK_USERNAME = ''                                # user login
    OAUTH_TOKENS_FACEBOOK_PASSWORD = ''                                # user password

Usage examples
--------------

...

Licensing
---------

This library uses the [Apache License, version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).
Please see the library's individual files for more information.
