# coding: utf-8
# GitHub siiway/serv00-daemon @ main : /script/install-daemon.py
'''
'DaemonKey_Placeholder'
'DaemonCommand_Placeholder'
'LogFile_Placeholder'

mkdir daemoninst && cd daemoninst
wget -O daemon.zip https://github.com/siiway/serv00-daemon/archive/refs/heads/main.zip # 下载本 repo
unzip daemon.zip # 解压
cp main/app/* ~/
'''
import os
# raise NotImplementedError('还没做完呢(')

# func
base = ''


def testcmd(cmd):
    '''
    success: True
    fail (not 0): False
    '''
    ret = os.system(f'{cmd}>/dev/null')
    if ret == 0:
        print(f'[debug / testcmd] test {cmd}: {ret} success')
        return True
    else:
        print(f'[debug / testcmd] test {cmd}: {ret} fail')
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
        raise f'Download file {url} to {path} failed! (Return code: {ret})'


def getpth(path=''):
    '''
    获取绝对路径
    '''
    ret = os.path.join(base, path)
    print(f'[debug / getpth] {path} -> {ret}')
    return ret


def unzip(zipfile, cwd=getpth()):
    print(f'[debug / unzip] unzip {zipfile} on {cwd}')
    ret = os.system(f'cd {cwd} && unzip {zipfile}')
    if ret:
        raise f'Unzip {zipfile} failed! (working: {cwd}, return: {ret})'

def move(src, dst):
    print(f'[debug / move] {src} -> {dst}')
    ret = os.system(f'mv -vf {src} {dst}')
    if ret:
        raise f'Move {src} to {dst} failed!'

def main():
    print('''
Serv00 Daemon Installer
https://github.com/siiway/serv00-daemon/blob/main/script/install-daemon.py
请在继续前安装: (wget 或 curl), unzip
''')
    print('请在 Devil 控制面板创建一个 Python 项目, 并在此输入路径 (如 "/home/wyf9/domains/daemon.wyf9.serv00.net/"):')
    base = input('> ')
    print('Step 1: 下载 repo')
    get('https://github.com/siiway/serv00-daemon/archive/refs/heads/main.zip', getpth('code.zip'))
    print('Step 2: 解压代码')
    unzip('code.zip')
    print('Step 3: 拷贝文件到正确位置')
    move(getpth('serv00-daemon-main/app/*'), getpth('public_python/'))
    print('Step 4:?')

main()
