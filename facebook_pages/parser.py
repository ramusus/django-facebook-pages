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
from facebook_api.parser import FacebookParser, FacebookParseError
import simplejson as json


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
