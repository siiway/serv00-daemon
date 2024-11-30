from os import name as osname
if osname == 'nt':
    exit(1)  # if running on Windows system, then quit.

from flask import Flask, request
import subprocess
from datetime import datetime

from index import *
from config import *

app = Flask(__name__)


def log(loginfo='', ip='(ip)', path='/(path)'):
    '''
    :param loginfo: 日志信息
    :param ip: 请求 ip, 一般为 `request.remote_addr` (先从 `flask` 库导入才可使用)
    :param path: 请求路径
    '''
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f'\n{"-"*16}\n[{datetime.now()}] [{ip}] {path}\n{loginfo}')


with open(LOG_FILE, 'w', encoding='utf-8') as f:
    f.write('')  # 以写入模式打开文件，清空 log 内容


@app.route("/")
def index():
    '''
    伪装根目录
    '''
    log(loginfo='Show Index Page', ip=request.remote_addr, path='/')
    return INDEX_HTML


@app.route('/daemon/<key>', methods=['GET', 'HEAD'])
def daemon(key):
    '''
    此处调起 pm2
    '''
    ret = '<!DOCTYPE HTML>\nServ00 Daemon Script'
    ret += f'\nBy wyf9, All rights Reserved.\n\n'
    if key != DAEMON_KEY:
        ret += f'Incorrect Key!\n'
    else:
        ret += f'DaemonCommand: {DAEMON_COMMAND}\n'
        try:
            # 使用 subprocess.PIPE 捕获输出
            callproc = subprocess.Popen(DAEMON_COMMAND, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = callproc.communicate()  # 获取输出和错误信息
            stdout = stdout.decode("utf-8")
            stderr = stderr.decode("utf-8")
            ret += f'ProcessStatus: \n'
            # 使用 returncode 获取进程返回状态
            ret += f'- running: {callproc.returncode}\n'
            ret += f'- pid: {callproc.pid}\n'
            ret += f'Output:\n---\n{stdout}\n'  # 将输出解码为字符串
            if stderr:
                # 将错误信息解码为字符串
                ret += f'---\nError: {stderr}\n'
        except Exception as e:
            ret += f'Error executing command: {str(e)}\n'
    if request.method == 'HEAD':
        # 处理 HEAD 请求
        ret = '(HEAD request)'
        if key != DAEMON_KEY:
            ret += f'\nIncorrect Key!'
    log(loginfo=ret, ip=request.remote_addr, path='/daemon')
    return f'<pre>{ret}</pre>'


if __name__ == "__main__":
    app.run()
