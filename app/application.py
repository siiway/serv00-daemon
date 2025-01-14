# coding: utf-8
'''
rm -r ./* && nano i.py && python3 i.py
devil www restart daemon.wyf9.serv00.net
↑ 这只是方便调试用的
'''

# from flask import Flask, request
import flask
import subprocess
import datetime

import indexpage
import config
import sshrenew

app = flask.Flask(__name__)


def log(loginfo: str = '', ip: str = '(ip)', method: str = '(method)', path: str = '/(path)'):
    '''
    :param loginfo: 日志信息
    :param ip: 请求 ip, 一般为 `request.remote_addr` (先从 `flask` 库导入才可使用)
    :param method: 请求方式 (get/post/...)
    :param path: 请求路径
    '''
    with open(config.LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f'\n{"-"*16}\n[{datetime.datetime.now().timestamp()}] [{ip}] {method} {path}\n{loginfo}')


with open(config.LOG_FILE, 'w', encoding='utf-8') as f:
    f.write('')  # 以写入模式打开文件，清空 log 内容


@app.route("/")
def index():
    '''
    伪装根目录
    '''
    log(loginfo='Show Index Page', ip=flask.request.remote_addr, path='/')
    return indexpage.INDEX_HTML


@app.route('/<path>/<key>', methods=['GET', 'HEAD', 'POST'])
def process(path: str, key: str):
    '''
    处理有效请求

    :param path: 路径 (就是要执行的操作, 可选 daemon 或 renew)
    :param key: 就是 DAEMON_KEY 啦
    '''
    ret = '''<!DOCTYPE HTML>
Serv00 Daemon Script
By wyf9, All rights Reserved.
https://github.com/siiway/serv00-daemon - Give a star⭐!\n
'''
    if key != config.DAEMON_KEY:
        ret += f'Incorrect Key!\n'
    else:
        match path.lower():
            case 'daemon':
                ret += f'DaemonCommand: {config.DAEMON_COMMAND}\n'
                try:
                    # 使用 subprocess.PIPE 捕获输出
                    callproc = subprocess.Popen(config.DAEMON_COMMAND, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = callproc.communicate()  # 获取输出和错误信息
                    stdout = stdout.decode("utf-8")  # 将输出解码为字符串
                    stderr = stderr.decode("utf-8")  # 将错误信息解码为字符串
                    ret += f'ProcessStatus: \n'
                    ret += f'- running: {callproc.returncode}\n'  # 使用 returncode 获取进程返回状态
                    ret += f'- pid: {callproc.pid}\n'
                    ret += f'Output (stdout):\n---\n{stdout}\n'
                    if stderr:
                        ret += f'---\Error (stderr): {stderr}\n'
                except Exception as e:
                    ret += f'ERROR executing command: {str(e)}\n'
            case 'renew':
                ret += sshrenew.login(config.SSH_COMMAND)
            case _:
                ret += f'ERROR: invaild path /{path}'
    log(loginfo=ret, ip=flask.request.remote_addr, method=flask.request.method, path=f'{path}')
    return f'<pre>{ret}</pre>'


if __name__ == "__main__":
    app.run()
