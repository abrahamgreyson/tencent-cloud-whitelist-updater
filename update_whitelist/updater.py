"""
Author: abe<wechat:abrahamgreyson>
Date: 2024/6/13 13:45:50
"""

from .cloud_providers.tencent_cloud import TencentCloud
from .cloud_providers.huawei_cloud import HuaweiCloud
from .logger import get_logger

logger = get_logger()


def update_cloud_providers(current_ip, config):
    """
    更新云服务商的白名单
    """
    # 遍历每个云服务提供商
    for provider_name, provider_config in config.dict().items():
        if provider_config is None:
            continue

        print(f"更新 {provider_name}...")
        access_key = provider_config['access_key']
        secret_key = provider_config['secret_key']

        # 遍历每个区域
        for region_config in provider_config['regions']:
            region = region_config['region']
            rules = region_config['rules']

            # 遍历每个安全组
            for rule in rules:
                sg = rule['sg']
                allows = rule['allow']

                # 取得现有安全组规则
                # 判断是否和配置一模一样
                # 删除所有备注， 然后根据配置全部新建
                provider_update_security_group(provider_name, access_key, secret_key, region, sg, current_ip, port)

                # # 遍历每个 allow
                # for allow in allows:
                #     port = allow['port']
                #
                #     print(f"Allow Port: {port}")
                #
                #     # 调用 provider 的更新方法，添加当前 IP 和端口规则
                #     print(f"更新安全组 {sg}，添加 IP {current_ip} 和端口 {port}...")

    return None


def provider_update_security_group(provider_name, access_key, secret_key, region, sg, ip, port):
    """
    调用云服务提供商的 API 更新安全组规则
    """
    # 这里根据 provider_name 调用不同的 provider 更新方法
    if provider_name == 'huawei':
        print('huawei')
        # update_huawei_security_group(access_key, secret_key, region, sg, ip)
    elif provider_name == 'tencent':
        print('tencent')
        # update_tencent_security_group(access_key, secret_key, region, sg, ip)
    elif provider_name == 'aliyun':
        print('aliyun')
        # update_aliyun_security_group(access_key, secret_key, region, sg, ip)
    # 添加其他 provider 的更新方法
