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


def login(command) -> str:
    '''
    自定义 SSH 函数\n
    ps: 如果想的话, 可以自己修改实现多个账号续期哦

    :param command: 配置中的 SSH_COMMAND
    :return: 多行日志信息
    '''
    log = '--- SSH Renew\n'
    message = ''
    try:
        # 使用 subprocess.PIPE 捕获输出
        callproc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # 读取输出和错误信息
        stdout, stderr = callproc.communicate(timeout=30)
        pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
        match = re.search(pattern, stdout)
        if match:
            expire = match.group(1)
            log += f'\nexpire: {expire}'
        else:
            expire = 'Failed to get expiration date'
            log += f'Failed to get expiration date\nOriginal output (stdout):\n---\n{stdout}\n'
            if stderr:
                log += f'---\nError (stderr): {stderr}\n'

    except Exception as e:
        log += f'ERROR executing command: {str(e)}\n'

    return log
