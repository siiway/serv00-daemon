# coding: utf-8
# SSH Renew script
# 如需自行修改请看下面 login() 函数的注释
'''
1. login
2. get info
3. split info
4. close conn
'''

from os import system

def login(command: str) -> str:
    '''
    自定义 SSH 函数

    :param command: 用户在 config.py (SSH_COMMAND) 设置的 ssh 登录命令
    :return: 多行日志信息
    '''
    system(command)
    pass