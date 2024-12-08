"""
Author: abe<wechat:abrahamgreyson>
Date: 2024/6/19 17:17:15
"""
import requests
import random
import os
from .logger import get_logger

IP_CACHE_FILE = 'ip_cache.txt'
logger = get_logger()


def get_current_ip():
    """
    通过 ipinfo.io 获取当前 IP 地址
    """
    api = ['https://ipinfo.io/ip?token=token_a', 'https://ipinfo.io/ip?token=token_b']
    url = random.choice(api)
    logger.info(f"通过 {url} 获取 IP")
    response = requests.get(url)
    if response.status_code == 200:
        logger.info(f"本机外网 IP：{response.text.strip()}")
        return response.text.strip()
    else:
        raise Exception(f"IP 获取失败. Status code: {response.status_code}")


def load_cached_ip():
    """
    读取缓存的 IP 地址
    """
    if os.path.exists(IP_CACHE_FILE):
        with open(IP_CACHE_FILE, 'r') as file:
            return file.read().strip()
    return None


def cache_ip(ip):
    """
    缓存当前 IP 地址
    """
    with open(IP_CACHE_FILE, 'w') as file:
        file.write(ip)
