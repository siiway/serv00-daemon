# coding: utf-8
# webhook.py: 自定义 Webhook 提醒

import subprocess
from discord_webhook import DiscordWebhook
import datetime
import pytz

import config


def hook(result: str) -> tuple[int, str]:
    '''
    Hook function

    :param success: 是否成功
    :param result: 运行结果
    :return: 请求返回
    :return[int]: 状态码
    :return[str]: 请求内容
    '''
    url = config.WEBHOOK_URL

    # 构造消息
    try:
        user = subprocess.check_output(["whoami"]).decode().strip()
    except:
        user = '[get user failed]'
    try:
        hostname = subprocess.check_output(["uname", "-n"]).decode().strip()
    except:
        hostname = '[get hostname failed]'
    try:
        time = datetime.datetime.now(pytz.timezone(config.TIMEZONE)).strftime('%Y-%m-%d %H:%M:%S')
    except pytz.UnknownTimeZoneError:
        time = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
        config.TIMEZONE = 'Asia/Shanghai [**Invaild timezone in config**]'
    message = f'''{"-"*45}
*[ **{user}** @ **{hostname}** ]*
> Serv00 Auto Renew Completed!
> **Execute time**: {time} *({config.TIMEZONE})*
> **Expire time**: {result} *({config.TIMEZONE})*
'''
    webhook = DiscordWebhook(url=url, content=message)
    response = webhook.execute()
    return response.status_code, response.text
