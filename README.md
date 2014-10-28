# Django Facebook Graph API Ads

[![Build Status](https://travis-ci.org/ramusus/django-facebook-pages.png?branch=master)](https://travis-ci.org/ramusus/django-facebook-pages) [![Coverage Status](https://coveralls.io/repos/ramusus/django-facebook-pages/badge.png?branch=master)](https://coveralls.io/r/ramusus/django-facebook-pages)

Application for interacting with Facebook Graph API Pages objects using Django model interface

## Installation

    pip install django-facebook-pages

Add into `settings.py` lines:

    INSTALLED_APPS = (
        ...
        'oauth_tokens',
        'facebook_api',
        'facebook_pages',
    )

    # oauth-tokens settings
    OAUTH_TOKENS_HISTORY = True                                        # to keep in DB expired access tokens
    OAUTH_TOKENS_FACEBOOK_CLIENT_ID = ''                               # application ID
    OAUTH_TOKENS_FACEBOOK_CLIENT_SECRET = ''                           # application secret key
    OAUTH_TOKENS_FACEBOOK_SCOPE = ['offline_access']                   # application scopes
    OAUTH_TOKENS_FACEBOOK_USERNAME = ''                                # user login
    OAUTH_TOKENS_FACEBOOK_PASSWORD = ''                                # user password

## Usage examples

### Fetch page by Graph ID

    >>> from facebook_pages.models import Page
    >>> page = Page.remote.fetch('19292868552')
    >>> page
    <Page: Facebook Developers>
    >>> page.__dict__
    {'_external_links_post_save': [],
     '_external_links_to_add': [],
     '_foreignkeys_post_save': [],
     '_state': <django.db.models.base.ModelState at 0xb1d718c>,
     'about': 'Grow your app with Facebook\nhttps://developers.facebook.com/ ',
     'can_post': False,
     'category': 'Product/service',
     'checkins': None,
     'company_overview': 'Facebook Platform enables anyone to build social apps on Facebook, mobile, and the web.\n\n',
     'cover': {'cover_id': '10151298218353553',
      'offset_x': 0,
      'offset_y': 0,
      'source': 'http://m.ak.fbcdn.net/sphotos-b.ak/hphotos-ak-ash4/s720x720/377655_10151298218353553_500025775_n.png'},
     'description': '',
     'graph_id': '19292868552',
     'id': 9,
     'is_published': True,
     'likes': 1225086,
     'link': 'http://www.facebook.com/FacebookDevelopers',
     'location': None,
     'name': 'Facebook Developers',
     'phone': '',
     'picture': '',
     'posts_count': 0,
     'products': '',
     'talking_about_count': 31550,
     'username': 'FacebookDevelopers',
     'website': 'http://developers.facebook.com'}

### Fetch and access page posts and comments

For this purpose you need to install dependency
[`django-facebook-posts`](http://github.com/ramusus/django-facebook-posts/) and add it into `INSTALLED_APPS`

    >>> from facebook_pages.models import Page
    >>> page = Page.remote.fetch('19292868552')
    >>> page.fetch_posts()
    [<Post: Facebook Developers: Excited for March Madness? We spoke with the folks at Pickmoto about their app to manage March Madness pools. Check out the interview.>,
     <Post: Facebook Developers: To help developers understand the updates we just announced to Timeline and Open Graph, we've published this three video series. Check it out!>,
     '...(remaining elements truncated)...']
    >>> page.wall_posts.count()
    354
    >>> page.wall_posts[0].fetch_comments()
    [<Comment: Comment object>, <Comment: Comment object>, <Comment: Comment object>, '...(remaining elements truncated)...']
    >>> page.wall_comments.count()
    16