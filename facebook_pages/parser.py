# -*- coding: utf-8 -*-
from facebook_api.parser import FacebookParser, FacebookParseError
from django.utils import simplejson as json

class FacebookPageFansParser(FacebookParser):

    @property
    def html(self):
        content = self.content
        response_instance = json.loads(content[9:])
        try:
            content = response_instance['domops'][0][3]['__html']
        except KeyError:
            if 'error' in response_instance:
                raise FacebookParseError(response_instance['error'], response_instance['errorDescription'])
            else:
                raise

        return content