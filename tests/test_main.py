"""
Author: abe<wechat:abrahamgreyson>
Date: 2024/6/25 11:34:49
"""

import pytest
from main import has_ip_changed, check_and_update_ip


def test_has_ip_changed(mocker):
    # 模拟 get_current_ip 和 load_cached_ip 函数的返回值
    mocker.patch('main.get_current_ip', return_value='1.1.1.1')
    mocker.patch('main.load_cached_ip', return_value='1.1.1.1')

    # 测试 has_ip_changed 函数
    ip_changed, current_ip = has_ip_changed()
    assert not ip_changed
    assert current_ip == '1.1.1.1'

    # 修改模拟函数的返回值
    mocker.patch('main.get_current_ip', return_value='2.2.2.2')

    # 再次测试 has_ip_changed 函数
    ip_changed, current_ip = has_ip_changed()
    assert ip_changed
    assert current_ip == '2.2.2.2'


def test_check_and_update_ip(mocker):
    # 模拟 has_ip_changed 函数的返回值
    mocker.patch('main.has_ip_changed', return_value=(True, '1.1.1.1'))

    # 创建一个模拟的 Updater 实例
    mock_updater = mocker.patch('main.Updater').return_value

    # 测试 check_and_update_ip 函数
    check_and_update_ip()

    # 检查 Updater 的 update_cloud_providers 方法是否被正确地调用了一次
    mock_updater.update_cloud_providers.assert_called_once()
