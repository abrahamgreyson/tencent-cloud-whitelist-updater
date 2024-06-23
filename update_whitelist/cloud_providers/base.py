"""
Author: abe<wechat:abrahamgreyson>
Date: 2024/6/13 11:00:36
"""

from abc import ABC, abstractmethod


class CloudProvider(ABC):
    @abstractmethod
    def update_rules(self, group_id, rules):
        """
        更新安全组规则
        """
        pass

    @abstractmethod
    def get_rules(self, group_id):
        """
        获取安全组规则
        """
        pass
