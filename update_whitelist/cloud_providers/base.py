"""
Author: abe<wechat:abrahamgreyson>
Date: 2024/6/13 11:00:36
"""

from abc import ABC, abstractmethod


class CloudProvider(ABC):
    @abstractmethod
    def update_security_group(self, group_id, rules):
        pass
