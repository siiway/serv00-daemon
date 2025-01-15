# coding: utf-8
# webhook.py: 自定义 Webhook 提醒

import subprocess
import requests
import datetime
import os
import json


import config


def hook(result: str) -> tuple[int, str]:
    '''
    Hook function

    :param success: 是否成功
    :param result: 运行结果 (正常情况下是时间戳!!)
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
    except Exception as e:
        user = f'[get user failed]: {e}'
    # hostname
    try:
        hostname = subprocess.check_output(["uname", "-n"]).decode().strip()
    except Exception as e:
        hostname = f'[get hostname failed]: {e}'
    # time now
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # days left
    try:
        data_result = result  # int(datetime.datetime.fromtimestamp(int(result)).timestamp())
        data_now = int(datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S').timestamp())
        time_str = f'<t:{data_now}:f> - <t:{data_now}:R>'
        expire_str = f'<t:{data_result}:f> - <t:{data_result}:R>'
    except Exception as e:
        time_str = f'[get time failed]: {e}'
        expire_str = f'[get expire failed]: {e} / raw: {result}'
    # pm2 status
    try:
        pm2_status = subprocess.check_output([os.path.expanduser("~/.npm-global/bin/pm2"), "status"]).decode().strip()
    except Exception as e:
        pm2_status = f'[get pm2 status failed]: {e}'
    if len(pm2_status) > 2000:
        pm2_status = '[pm2 status string is too long (> 2000 chars)]'
    # build request
    headers = {
        'Content-Type': 'application/json'
    }
    Json = {
        'embeds': [
            {
                'title': f'[**`{user}`**] Serv00 Auto Renew Completed!',
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
                        'name': 'Expire',
                        'value': expire_str,
                        'inline': True
                    }
                ],
                'description': f'```\n{pm2_status}\n```'
            }
        ]
    }
    try:
        print(json.dumps(Json, ensure_ascii=False))
        response = requests.post(url=url, headers=headers, json=Json)
    except Exception as e:
        return -1, f'{e}'
    return response.status_code, response.text
