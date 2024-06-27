"""
Author: abe<wechat:abrahamgreyson>
Date: 2024/6/25 12:14:39
"""

import pytest
from unittest.mock import Mock, patch
from update_whitelist.updater import Updater
from update_whitelist.cloud_providers.tencent_cloud import TencentCloud
from update_whitelist.cloud_providers.huawei_cloud import HuaweiCloud


def test_update_cloud_providers(mocker):
    mocker.patch.object(Updater, 'set_client')
    mocker.patch.object(Updater, 'update_security_group_rules')
    updater = Updater()
    config = {
        'tencent': {
            'access_key': 'key1',
            'secret_key': 'secret1',
            'regions': [
                {
                    'region': 'region1',
                    'rules': [
                        {
                            'sg': 'sg1',
                            'allow': ['allow1']
                        }
                    ]
                }
            ]
        }
    }
    # 创建一个 MagicMock 对象，并设置其 .dict() 方法返回 config
    config_mock = mocker.MagicMock()
    config_mock.dict.return_value = config
    updater.update_cloud_providers('127.0.0.1', config_mock)
    updater.set_client.assert_called_once_with('tencent', 'key1', 'secret1', 'region1')
    updater.update_security_group_rules.assert_called_once_with('sg1', ['allow1'], '127.0.0.1')


def test_update_security_group_rules_with_existed_rules(mocker):
    updater = Updater()
    updater.client = Mock()
    mocker.patch.object(updater, 'fetch_security_group_rules', return_value=['rule1'])
    updater.update_security_group_rules('sg1', ['allow1'], '127.0.0.1')
    updater.client.delete_rules.assert_called_once_with('sg1', ['rule1'])
    updater.client.add_rules.assert_called_once_with('sg1', ['allow1'], '127.0.0.1')


def test_update_security_group_rules_without_existed_rules(mocker):
    updater = Updater()
    updater.client = Mock()
    mocker.patch.object(updater, 'fetch_security_group_rules', return_value=[])
    updater.update_security_group_rules('sg1', ['allow1'], '127.0.0.1')
    updater.client.delete_rules.assert_not_called()
    updater.client.add_rules.assert_called_once_with('sg1', ['allow1'], '127.0.0.1')


def test_set_client(mocker):
    updater = Updater()
    # 创建一个模拟的 TencentCloud 对象
    mock_tencent_cloud = mocker.MagicMock(spec=TencentCloud)
    # 使用模拟的 TencentCloud 对象替代真实的 TencentCloud 类
    mocker.patch('update_whitelist.updater.TencentCloud', return_value=mock_tencent_cloud)
    updater.set_client('tencent', 'key1', 'secret1', 'region1')
    assert isinstance(updater.client, TencentCloud)
    # 创建一个模拟的 HuaweiCloud 对象
    mock_huawei_cloud = mocker.MagicMock(spec=HuaweiCloud)
    # 使用模拟的 HuaweiCloud 对象替代真实的 HuaweiCloud 类
    mocker.patch('update_whitelist.updater.HuaweiCloud', return_value=mock_huawei_cloud)
    updater.set_client('huawei', 'key2', 'secret2', 'ae-ad-1')
    assert isinstance(updater.client, HuaweiCloud)
    with pytest.raises(ValueError):
        updater.set_client('unsupported', 'key', 'secret', 'region')


def test_fetch_security_group_rules(mocker):
    updater = Updater()
    updater.client = Mock()
    updater.client.get_rules.return_value = ['rule1']
    assert updater.fetch_security_group_rules('sg1') == ['rule1']
    updater.client.get_rules.side_effect = Exception('error')
    with patch('update_whitelist.updater.logger') as mock_logger:
        assert updater.fetch_security_group_rules('sg1') is None
        mock_logger.error.assert_called_once_with('获取 sg1 安全组规则时出错: error')
