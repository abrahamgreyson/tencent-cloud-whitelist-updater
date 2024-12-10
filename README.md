# 定时更新云服务安全组规则

[![Test](https://github.com/abrahamgreyson/whitelist_updater/actions/workflows/test.yml/badge.svg)](https://github.com/abrahamgreyson/whitelist_updater/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/abrahamgreyson/whitelist_updater/branch/main/graph/badge.svg?token=Fc4MbBmMpZ)](https://codecov.io/gh/abrahamgreyson/whitelist_updater)

这个工具旨在在缺乏堡垒机的情况下，对在线服务器放行本地 ip，免得长期暴露敏感端口。它会定时（每 3 分钟）获取本地的外网 ip，更新到云服务器的安全组白名单（目前支持腾讯云、华为云，其它云请自己实现接口）。
支持多个云，每个云支持多个 region，每个 region 支持多个安全组，每个安全组支持多个端口的放行。

## 部署

1. 基于 Python 3.12 开发（推荐使用 3.12+），如果低于 3.12 也必须使用 3.10 以上，因为我们使用了联合类型 `str | int` 这种，请注意，并没有针对 3.10 和  3.11 进行测试
2. 安装依赖 `pip install -r requirements.txt`
3. 复制模板配置文件 `config.example.yaml` 到 `config.yaml`，按需配置（请看下一节配置章节）
4. 运行

  ```bash
   # 调试模式运行，带有 stdout
   python main.py
   
   # 后台运行、丢弃任何输出（活着使用 screen 活 tmux 工具能达到同样效果）
   nohup python main.py > /dev/null 2>&1 &
      
   # 验证是否执行
   ps aux | grep python
   
   # 重要服务，建议新建 systemd 服务单元，可以保证开机启动，也更好使用 systemctl 管理
   # 新建服务单元配置
   sudo vim /etc/systemd/system/whitelist.service
   # 文件添加下个代码段的内容👇 ， 按需更改其中路径
   
   # 重新加载 systemd 配置
   sudo systemctl daemon-reload
   # 启动服务
   sudo systemctl start whitelist
   # 开机自启
   sudo systemctl enable whitelist
   # 检查状态 
   sudo systemctl status whitelist
   ```

   ```ini
   [Unit]
   Description=Update whitelist by Abe
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /path/to/your/main.py
   WorkingDirectory=/path/to/your/
   # 丢弃 stderr 和 stdout， 我们自己维护日志
   StandardOutput=null
   StandardError=null
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

## 配置

### ipinfo.io

我们使用 ipinfo 的服务，去获得本地外网 ip， 最好申请个 token， 这样可以有更多的 rate limit 上限。

### 华为云

在[统一身份认证服务 IAM](https://console.huaweicloud.com/iam/?agencyId=c79cb5a07cda49f9bb4c4f7d97d4d506&region=cn-east-3&locale=zh-cn#/iam/users) 中创建用户，赋予特定的接口权限，获取用户的 `Access Key` 和 `Secret Key`。

我们使用到的华为云 VPC 接口有：

- `ListSecurityGroupRule`
- `DeleteSecurityGroupRule`
- `BatchCreateSecurityGroupRules`

我们需要放行的权限：

```json
{
    "Version": "1.1",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "vpc:securityGroupRules:create",
                "vpc:securityGroupRules:delete",
                "vpc:securityGroupRules:get"
            ]
        }
    ]
}
```

#### 腾讯云

在[访问管理](https://console.cloud.tencent.com/cam/overview)中创建用户，赋予特定的接口权限，获取用户的 `SecretId` 和 `SecretKey`。

我们使用到的接口：

- `DescribeSecurityGroupPolicies`
- `DeleteSecurityGroupPolicies`
- `CreateSecurityGroupPolicies`

我们需要放行的权限：

```json
{
  "statement": [
    {
      "action": [
        "cvm:DescribeSecurityGroup*",
        "cvm:Create*",
        "cvm:DeleteSecurityGroupPolicy"
      ],
      "effect": "allow",
      "resource": [
        "*"
      ]
    }
  ],
  "version": "2.0"
}
```

## 扩展

因为是自用的，所以仅实现了腾讯和华为云，如果你使用其它云平台，请按照 `update_whitelist/cloud_providers` 目录下的现有代码实现自己的云服务供应商，需要实现的方法签名如下。 为了更加快捷地实现这些方法， 可以直接去云服务商的 API 调试台，先搞清楚接口什么怎么调用的，然后直接引入其 sdk 即可。

```python
    @abstractmethod
    def initialize_client(self):
        """
        初始化特定云服务的客户端
        """
    pass

    @abstractmethod
    def delete_rules(self, group_id, rules):
        """
        删除安全组规则
        """
        pass

    @abstractmethod
    def add_rules(self, group_id, rules, ip):
        """
        添加安全组规则
        """
        pass

    @abstractmethod
    def get_rules(self, group_id):
        """
        获取安全组规则
        """
        pass
```
  
## 测试

```bash
# 安装开发依赖
pip install -e ".[dev]"
# 运行
pytest
```

## LICENSE

MIT
