# coding: utf-8
# SSH Renew script
# 如需自行修改请看下面 login() 函数的注释
'''
1. login
2. get info
3. split info
4. close conn
'''

import subprocess


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
        stdout, stderr = callproc.communicate(input='exit 0\n', timeout=10)

        log += f'ProcessStatus: \n'
        log += f'- running: {callproc.returncode}\n'  # 使用 returncode 获取进程返回状态
        log += f'- pid: {callproc.pid}\n'
        log += f'Output (stdout):\n---\n{stdout}\n'
        if stderr:
            log += f'---\nError (stderr): {stderr}\n'

    except Exception as e:
        log += f'ERROR executing command: {str(e)}\n'

    return log
