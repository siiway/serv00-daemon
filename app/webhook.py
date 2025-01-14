# coding: utf-8
# webhook.py: 自定义 Webhook 提醒

import subprocess
from discord_webhook import DiscordWebhook  # type: ignore
import datetime

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

    # 判断是否启用
    if not url:
        return 0, 'Hook Disabled'

    # 构造消息
    # user
    try:
        user = subprocess.check_output(["whoami"]).decode().strip()
    except:
        user = '[get user failed]'
    # hostname
    try:
        hostname = subprocess.check_output(["uname", "-n"]).decode().strip()
    except:
        hostname = '[get hostname failed]'
    # time now
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # days left
    try:
        date1 = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        date2 = datetime.datetime.strptime(result, '%Y-%m-%d %H:%M:%S')
        time_str = f'<t:{date1.timestamp()}:f> - <t:{date1.timestamp()}:R>'
        expire_str = f'<t:{date2.timestamp()}:f> - <t:{date2.timestamp()}:R>'
    except:
        expire_str = '[get expire failed]'
    # pm2 status
    try:
        pm2_status = subprocess.check_output(["pm2", "status"]).decode().strip()
    except:
        pm2_status = '[get pm2 status failed]'
    # build embeds
    embeds = [
        {
            'title': f'[**{user}**] **Serv00 Auto Renew Completed!**',
            'fields': [
                {
                    'name': 'Time',
                    'value': time_str,
                    'inline': True
                },
                {
                    'name': 'Hostname',
                    'value': hostname,
                    'inline': True
                },
                {
                    'name': 'User',
                    'value': user,
                    'inline': True
                },
                {
                    'name': 'Result',
                    'value': result,
                    'inline': True
                },
                {
                    'name': 'Expire',
                    'value': expire_str,
                    'inline': True
                },
                {
                    'name': 'PM2 Status',
                    'value': f'```\n{pm2_status}\n```',
                    'inline': False
                }
            ]
        }
    ]
    webhook = DiscordWebhook(url=url, embeds=embeds)
    try:
        response = webhook.execute()
    except Exception as e:
        return -1, f'{e}'
    return response.status_code, response.text
