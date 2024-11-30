# coding: utf-8
# GitHub siiway/serv00-daemon @ main : /script/install-daemon.py
'''
'DaemonKey_Placeholder'
'DaemonCommand_Placeholder'
'LogFile_Placeholder'
'''
import os
from uuid import uuid4 as uuid


def testcmd(cmd):
    '''
    success: True
    fail (not 0): False
    '''
    ret = os.system(f'{cmd}>/dev/null')
    if ret == 0:
        return True
    else:
        return False


def get(url, path):
    '''
    返回非 0 则失败?
    '''
    if testcmd('wget --version'):
        cmd = f'wget -O {path} {url}'
    elif testcmd('curl --version'):
        cmd = f'curl -o {path} {url}'
    else:
        raise FileNotFoundError('无法找到 wget 或 curl 作为下载支持, 请先安装其一!')
    ret = os.system(cmd)
    if ret:
        raise Exception(f'Download file {url} to {path} failed! (Return code: {ret})')


def getpth(path=''):
    '''
    获取绝对路径
    '''
    ret = os.path.join(base, path)
    return ret


def unzip(zipfile, cwd=None):
    if not cwd:
        cwd = getpth()
    ret = os.system(f'cd {cwd} && unzip -o {zipfile}')
    if ret:
        raise Exception(f'Unzip {zipfile} failed! (working: {cwd}, return: {ret})')


def copy(src, dst):
    ret = os.system(f'cp {src} {dst}')
    if ret:
        raise Exception(f'Copy {src} to {dst} failed!')


def user_input(name, desc, default):
    print(f'[Input] {name}: {desc} / 默认: {default}')
    ret = input(f'> {name}: ')
    if not ret:
        ret = default
    return ret


def replace(value: str, before, after):
    '''
    before = aaa, after = bbb:
    'aaa' -> 'bbb'
    '''
    before = f"'{before}'"
    after = f"'{after}'"
    return value.replace(before, after)


def main():
    print('''
Serv00 Daemon Installer
https://github.com/siiway/serv00-daemon/blob/main/script/install-daemon.py
Repo: siiway/serv00-daemon
Give a Star ⭐ please~
''')
    print('请在 Devil 控制面板 (s*.serv00.com) 创建一个 Python 项目, \n[Input] 并在此输入路径 (如 "/home/wyf9/domains/daemon.wyf9.serv00.net/"):')
    global base
    base = input('> ')
    print('\nStep 0: 检查 pm2')
    if testcmd('pm2 --version'):
        print('检测到 pm2 已安装, 跳过下载')
    else:
        print('执行 pm2 --version 失败, 从 https://raw.githubusercontent.com/siiway/serv00-daemon/main/script/install-pm2.sh 下载')
        get('https://raw.githubusercontent.com/siiway/serv00-daemon/main/script/install-pm2.sh', getpth('install-pm2.sh'))
        os.system(f'bash {getpth("install-pm2.sh")}')
    print('Step 1: 下载 repo')
    get('https://github.com/siiway/serv00-daemon/archive/refs/heads/main.zip', getpth('code.zip'))
    print('Step 2: 解压代码')
    unzip('code.zip')
    print('Step 3: 拷贝文件到正确位置')
    copy(getpth('serv00-daemon-main/app/*'), getpth('public_python/'))
    print('Step 4: 设置参数')
    configpth = getpth("public_python/config.py")
    print(f'[Tip] 可以稍候编辑 {configpth} 以修改配置.')
    global file
    file = ''
    with open(configpth, mode='r', encoding='utf-8') as f:
        file = f.read()
        f.close()
    DaemonKey = user_input(name='DaemonKey', desc='访问时需要携带的 key (妥善保管)', default=uuid())
    print(f'设置的 key: {DaemonKey}')
    DaemonCommand = user_input(name='DaemonCommand', desc='访问时需要执行的命令', default='pm2 resurrect')
    LogFile = user_input(name='LogFile', desc='日志文件的路径', default='/dev/null')
    file = replace(file, 'DaemonKey_Placeholder', DaemonKey)
    file = replace(file, 'DaemonCommand_Placeholder', DaemonCommand)
    file = replace(file, 'LogFile_Placeholder', LogFile)
    with open(configpth, mode='w', encoding='utf-8') as f:
        f.write(file)
        f.close()


if __name__ == '__main__':
    main()
    print('安装成功!')
    print('Visit: https://github.com/siiway/serv00-daemon?tab=readme-ov-file#继续')
    print()
