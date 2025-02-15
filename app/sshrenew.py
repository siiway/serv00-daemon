# coding: utf-8
# sshrenew.py: SSH Renew script
# 如需自行修改请看下面 login() 函数的注释
'''
1. login
2. get info
3. split info
4. close conn
'''

import subprocess
import re
import datetime

import webhook


def login(command) -> str:
    '''
    自定义 SSH 函数\n
    ps: 如果想的话, 可以自己修改实现多个账号续期哦

    :param command: 配置中的 SSH_COMMAND
    :return: 多行日志信息
    '''
    log = '--- SSH Renew\n'
    try:
        # 使用 subprocess.PIPE 捕获输出
        callproc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # 读取输出和错误信息
        stdout, stderr = callproc.communicate(timeout=60)
        pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
        match = re.search(pattern, stdout)
        if match:
            result = match.group(1)
            # convert timezone
            result = int(datetime.datetime.strptime(result, '%Y-%m-%d %H:%M:%S').timestamp())
            log += f'\nExpire date now: {result}'
        else:
            result = 'Failed to parse expiration date'
            log += f'Failed to parse expiration date\nOriginal output (stdout):\n---\n{stdout}\n'
            if stderr:
                result = 'Detected stderr output when running command'
                log += f'---\nError (stderr): {stderr}\n'

    except Exception as e:
        result = f'Error executing command: {str(e)}'
        log += f'ERROR executing command: {str(e)}\n'
    print(f'result: `{result}`')
    hookcode, hookresp = webhook.hook(result=str(result))
    log += f'\nWebhook response: {hookcode}\n{hookresp}'
    return log
