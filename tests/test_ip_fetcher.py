"""
Author: abe<wechat:abrahamgreyson>
Date: 2024/6/25 16:27:03
"""

import pytest
from unittest.mock import patch
from update_whitelist.ip_fetcher import get_current_ip, load_cached_ip, cache_ip


def test_get_current_ip(mocker):
    # 创建一个模拟的 requests.get 响应
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.text = '127.0.0.1\n'
    # 使用模拟的响应替代 requests.get
    mocker.patch('requests.get', return_value=mock_response)
    assert get_current_ip() == '127.0.0.1'


def test_load_cached_ip(mocker):
    # 使用模拟的 open 替代内置的 open
    mocker.patch('builtins.open', mocker.mock_open(read_data='127.0.0.1\n'))
    assert load_cached_ip() == '127.0.0.1'


def test_cache_ip(mocker):
    # 创建一个模拟的文件对象
    mock_file = mocker.mock_open()
    # 使用模拟的文件对象替代内置的 open
    mocker.patch('builtins.open', mock_file)
    cache_ip('127.0.0.1')
    mock_file().write.assert_called_once_with('127.0.0.1')
