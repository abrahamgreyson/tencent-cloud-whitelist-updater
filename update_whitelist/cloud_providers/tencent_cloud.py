"""
Author: abe<wechat:abrahamgreyson>
Date: 2024/6/13 11:00:59
"""

from .base import CloudProvider


class TencentCloud(CloudProvider):
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def update_security_group(self, group_id, rules):
        pass

