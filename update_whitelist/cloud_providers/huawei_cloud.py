# coding: utf-8
"""
Author: abe<wechat:abrahamgreyson>
Date: 2024/6/13 11:01:15
"""

from .base import CloudProvider
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkvpc.v2 import VpcClient, ListVpcsRequest
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
from huaweicloudsdkcore.exceptions import exceptions
from update_whitelist.config import config


class HuaweiCloud(CloudProvider):
    def update_rules(self, group_id, rules):
        pass

    def get_rules(self, group_id):
        """
        获取安全组规则
        """
        credentials = BasicCredentials(config.huawei.access_key, config.huawei.secret_key)
        # 创建服务客户端
        client = VpcClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(VpcRegion.value_of(config.huawei.region)) \
            .build()

        # 发送请求并获取响应
        try:
            request = ListVpcsRequest()
            response = client.list_vpcs(request)
            print(response)

        except exceptions.ClientRequestException as e:
            print(e.status_code)
            print(e.request_id)
            print(e.error_code)
            print(e.error_msg)
