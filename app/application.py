from os import name as osname
if osname == 'nt':
    exit(1)  # if running on Windows system, then quit.

from flask import Flask, request
import subprocess
from datetime import datetime

from index import *
from config import *

app = Flask(__name__)
r = '<br\>\n'  # html 换行


def load_key(path, coding='utf-8'):
    '''
    :param path: 文件路径
    :param coding: 文件编码 (默认 utf-8)

    **包含用户目录时请用 `expanduser()` 扩展**
    '''
    with open(path, 'r', encoding=coding) as f:
        return f.read().strip()  # 从文件中读取 daemon_key


def log(loginfo='', ip='(ip)', path='/(path)'):
    '''
    :param loginfo: 日志信息
    :param ip: 请求 ip, 一般为 `request.remote_addr` (先从 `flask` 库导入才可使用)
    :param path: 请求路径
    '''
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f'\n{"-"*16}\n[{datetime.now()}] [{ip}] {path}\n{loginfo}')


# ---------- configs start
# 访问用 key
# DAEMON_KEY = load_key(expanduser('~/daemon.key'))
# DAEMON_KEY = 'DaemonKey_Placeholder'
# # 启动命令
# # DAEMON_COMMAND = 'pm2 resurrect'
# DAEMON_COMMAND = 'DaemonCommand_Placeholder'
# # 日志文件 (包含用户目录时请用 expanduser() 扩展)
# # LOG_FILE = expanduser('~/daemon.log')
# LOG_FILE = 'LogFile_Placeholder'
# # 伪装用根目录返回 (默认: Welcome to Nginx)
# INDEX_HTML = '''
# '''
# ---------- configs end


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
    ret += f'{r}By wyf9, All rights Reserved.{r}{r}'
    if key != DAEMON_KEY:
        ret += f'Incorrect Key!{r}'
    else:
        ret += f'DaemonCommand: {DAEMON_COMMAND}{r}'
        try:
            # 使用 subprocess.PIPE 捕获输出
            callproc = subprocess.Popen(DAEMON_COMMAND, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = callproc.communicate()  # 获取输出和错误信息
            stdout = stdout.decode("utf-8").replace('\n', r)
            stderr = stderr.decode("utf-8").replace('\n', r)
            ret += f'ProcessStatus: {r}'
            # 使用 returncode 获取进程返回状态
            ret += f'- running: {callproc.returncode}{r}'
            ret += f'- pid: {callproc.pid}{r}'
            ret += f'Output:{r}---{r}{stdout}{r}'  # 将输出解码为字符串
            if stderr:
                # 将错误信息解码为字符串
                ret += f'---{r}Error: {stderr}{r}'
        except Exception as e:
            ret += f'Error executing command: {str(e)}{r}'
    if request.method == 'HEAD':
        # 处理 HEAD 请求
        ret = '(HEAD request)'
        if key != DAEMON_KEY:
            ret += f'{r}Incorrect Key!'
    log(loginfo=ret, ip=request.remote_addr, path='/daemon')
    return ret.replace(' ', '&nbsp;')


if __name__ == "__main__":
    app.run()