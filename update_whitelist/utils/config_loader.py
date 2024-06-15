"""
Author: abe<wechat:abrahamgreyson>
Date: 2024/6/13 11:21:31
"""

import yaml


def load_config(config_path='config/config.yaml'):
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config
