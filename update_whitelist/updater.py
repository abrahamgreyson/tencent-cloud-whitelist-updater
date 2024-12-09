"""
Author: abe<wechat:abrahamgreyson>
Date: 2024/6/13 13:45:50
"""

from .cloud_providers.tencent_cloud import TencentCloud
from .cloud_providers.huawei_cloud import HuaweiCloud
from .logger import get_logger

logger = get_logger()


class Updater:
    client = None

    def update_cloud_providers(self, current_ip, config):
        """
        更新云服务商的白名单
        """

        # 遍历每个云服务提供商
        for provider_name, provider_config in config.dict().items():
            if provider_config is None or provider_name == 'ipinfo':
                continue

            logger.info(f"更新 {provider_name}...")
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

                    # 我Men以安全组为单位去初始化云服务客户端
                    self.set_client(provider_name, access_key, secret_key, region)
                    # 更新规则
                    self.update_security_group_rules(sg, allows, current_ip)
        return None

    def update_security_group_rules(self, sg, rules, ip):
        """
        更新安全组规则
        我们读出安全组规则，然后根据备注，把符合条件的全部删除，然后重新添加
        """
        logger.info(f"获取安全组 {sg} 的规则...")
        existed_rules = self.fetch_security_group_rules(sg)
        if existed_rules:
            # 删除所有规则
            logger.info(f"有符合条件的规则，删除安全组 {sg} 的所有规则...")
            self.client.delete_rules(sg, existed_rules)
            pass
        else:
            logger.info(f"安全组 {sg} 没有符合条件的规则，跳过删除...")
            pass
        # 删完了就按照配置文件再加进去
        logger.info(f"添加安全组 {sg} 的规则...")
        self.client.add_rules(sg, rules, ip)

        # 遍历每个 allow
        # for allow in allows:
        #     port = allow['port']
        #
        #     print(f"Allow Port: {port}")
        #
        #     # 调用 provider 的更新方法，添加当前 IP 和端口规则
        #     print(f"更新安全组 {sg}，添加 IP {current_ip} 和端口 {port}...")
        return None

    def set_client(self, provider_name, access_key, secret_key, region) -> None:
        """
        设置云服务客户端
        """
        if provider_name == 'huawei':
            self.client = HuaweiCloud(access_key, secret_key, region)
        elif provider_name == 'tencent':
            self.client = TencentCloud(access_key, secret_key, region)
        elif provider_name == 'aliyun':
            # 如果您还没有实现阿里云，我们可以暂时抛出一个异常
            raise NotImplementedError("阿里云安全组规则获取尚未实现")
        else:
            raise ValueError(f"不支持的云服务提供商: {provider_name}")

    def fetch_security_group_rules(self, sg):
        """
        获取安全组规则
        """
        try:
            # 调用相应云服务的方法获取安全组规则
            rules = self.client.get_rules(sg)
            logger.info(f"成功获取安全组 {sg} 的规则")
            print(rules)
            return rules

        except Exception as e:
            logger.error(f"获取 {sg} 安全组规则时出错: {str(e)}")
            return None
