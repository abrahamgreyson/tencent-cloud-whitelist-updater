"""
Author: abe<wechat:abrahamgreyson>
Date: 2024/6/13 16:40:14
"""
import os

import yaml
from pydantic import BaseModel
from typing import List, Optional


class Allow(BaseModel):
    ip: str
    port: int


class Rule(BaseModel):
    sg: str
    allow: List[Allow]


class CloudProvider(BaseModel):
    region: str
    access_key: str
    secret_key: str
    rules: List[Rule]


class Config(BaseModel):
    huawei: CloudProvider
    tencent: CloudProvider
    aliyun: CloudProvider


# 读配置文件
current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(current_path)
config_path = os.path.join(root_path, 'config.yaml')
with open(config_path, 'r') as file:
    config_data = yaml.safe_load(file)
config = Config(**config_data)

