# coding: utf-8
# SSH Renew script
# 如需自行修改请看下面 login() 函数的注释
'''
1. login
2. get info
3. split info
4. close conn
'''

import paramiko
from time import sleep
from config import *


def login() -> str:
    '''
    自定义 SSH 函数\n
    ps: 如果想的话, 可以自己修改实现多个账号续期哦

    :return: 多行日志信息
    '''
    log = '--- SSH Renew'

    hostname = 'localhost'
    port = 22
    username = USER_NAME
    private_key_path = SSH_KEY_PATH

    try:
        private_key = paramiko.RSAKey(filename=private_key_path)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(hostname, port, username, pkey=private_key)

        # MOTD command
        stdin, stdout, stderr = client.exec_command('source /etc/profile')
        sleep(10)
        # get full out
        out = stdout.read().decode()
        err = stderr.read().decode()

        log += f'\n\n{out}'
        if err:
            log += f'\n\nstderr:\n{err}'

        # 关闭SSH连接
        client.close()
    except Exception as e:
        log += f'\nERROR: {e}'
    return log
