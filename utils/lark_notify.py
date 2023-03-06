#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: lark_notify
@Created: 2023/2/17 17:15
"""

import json
import logging
import time
import requests
import urllib3

from utils import config
from utils.allure_fun import TestMetrics

urllib3.disable_warnings()

try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError


def is_not_null_and_blank_str(content):
    """
  非空字符串
  :param content: 字符串
  :return: 非空 - True，空 - False
  """
    return bool(content and content.strip())


class FeiShuTalkChatBot:
    """飞书机器人通知"""

    def __init__(self, metrics: TestMetrics):
        self.metrics = metrics

    def send_text(self, msg: str):
        """
    消息类型为text类型
    :param msg: 消息内容
    :return: 返回消息发送结果
    """
        data = {"msg_type": "text", "at": {}}
        if is_not_null_and_blank_str(msg):  # 传入msg非空
            data["content"] = {"text": msg}
        else:
            logging.error("text类型，消息内容不能为空！")
            raise ValueError("text类型，消息内容不能为空！")

        logging.debug('text类型：%s', data)
        return self.post()

    def post(self):
        """
    发送消息（内容UTF-8编码）
    :return: 返回消息发送结果
    """
        rich_text = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "【PyAuto测试通知】",
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "text": "测 试 项 目 : "
                                },
                                {
                                    "tag": "text",
                                    "text": f"{config.project_name}"
                                }
                            ],
                            [
                                {
                                    "tag": "text",
                                    "text": "测 试 人 员 : "
                                },
                                {
                                    "tag": "text",
                                    "text": f"{config.tester_name}"
                                }
                            ],
                            [
                                {
                                    "tag": "text",
                                    "text": "用 例 总 数 : "
                                },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.total}"
                                }
                            ],

                            [{
                                "tag": "text",
                                "text": "成 功 用 例 数 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.passed}"
                            }],  # 成功用例数

                            [{
                                "tag": "text",
                                "text": "失 败 用 例 数 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.failed}"
                            }],  # 失败用例数
                            [{
                                "tag": "text",
                                "text": "异 常 用 例 数 : "
                                },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.broken}"
                            }],  # 损坏用例数
                            [{
                                "tag": "text",
                                "text": "重 测 用 例 数 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.retry}"
                                }],  # 损坏用例数
                            [{
                                "tag": "text",
                                "text": "成 功 率 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.pass_rate} %"
                            }],  # 成功率
                            [
                                {
                                    "tag": "text",
                                    "text": "时 长 : "
                                },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.time}\n"
                                },
                                {
                                    "tag": "at",
                                    "user_id": "all",
                                }
                            ],
                        ]
                    }
                }
            }
        }
        headers = {'Content-Type': 'application/json; charset=utf-8'}

        post_data = json.dumps(rich_text)
        response = requests.post(
            config.lark.webhook,
            headers=headers,
            data=post_data,
            verify=False
        )
        result = response.json()

        if result.get('StatusCode') != 0:
            time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            result_msg = result['errmsg'] if result.get('errmsg', False) else '未知异常'
            error_data = {
                "msgtype": "text",
                "text": {
                    "content": f"[注意-自动通知]飞书机器人消息发送失败，时间：{time_now}，"
                               f"原因：{result_msg}，请及时跟进，谢谢!"
                },
                "at": {
                    "isAtAll": False
                }
            }
            logging.error("消息发送失败，自动通知：%s", error_data)
            requests.post(config.lark.webhook, headers=headers, data=json.dumps(error_data))
        return result

