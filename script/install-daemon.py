# coding: utf-8
# GitHub siiway/serv00-daemon - /script/install-daemon.py
# by wyf9. / **抄袭不标出处是一种可耻的行为** / https://github.com/siiway/serv00-daemon/blob/968ef1b4d45a4a9c51db9216c506288ed4bb5e14/script/install-pm2-saika-nobase64.sh#L12

import os
from uuid import uuid4 as uuid


def testcmd(cmd: str):
    '''
    执行命令, 判断 return code 是否为 0

    :param cmd: 要测试返回的命令
    :return True: success
    :return False: failed
    '''
    ret = os.system(f'{cmd}>/dev/null')
    if ret == 0:
        return True
    else:
        return False


def get(url: str, path: str):
    '''
    使用 wget 或 curl 下载文件
    > 返回非 0 则失败?

    :param url: 文件 url
    :param path: 将保存到的路径 (包括文件名)
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


def getpth(path: str = '') -> str:
    '''
    获取绝对路径

    :param path: 相对路径
    :return: `os.path.join()` 后的结果
    '''
    ret = os.path.join(base, path)
    return ret


def unzip(zipfile: str, cwd: str = None) -> str:
    '''
    调用 unzip 命令解压 zip 文件

    :param zipfile: zip 文件名
    :param cwd: 执行命令的目录
    '''
    if not cwd:
        cwd = getpth()
    ret = os.system(f'cd {cwd} && unzip -o {zipfile}')
    if ret:
        raise Exception(f'Unzip {zipfile} failed! (working: {cwd}, return: {ret})')


def copy(src: str, dst: str) -> str:
    ret = os.system(f'cp {src} {dst}')
    if ret:
        raise Exception(f'Copy {src} to {dst} failed!')


def user_input(name: str, place: str, desc: str, default: str, file: str) -> str:
    '''
    获取用户输入, 并替换文件中的 Placeholder (用 `''` 包裹)

    :param name: 显示给用户的名称
    :param place: 将被替换的值
    :param desc: 显示给用户的描述
    :param default: 用户未填写时返回的默认值
    :param file: 文件内容的字符串
    :return: 替换后的字符串
    '''
    print(f'[Input] {name}: {desc} / 默认: {default}')
    ret = input(f'> {name}: ')
    if not ret:
        ret = default
    before = f"'{place}'"
    after = f"'{ret}'"
    return file.replace(before, after)


def main():
    branch = 'dev'  # 当在 dev 分支调试安装脚本时我是崩溃的，所以又加了这个
    print(f'''
[INSTALL]
Serv00 Daemon Installer
https://github.com/siiway/serv00-daemon/blob/{branch}/script/install-daemon.py
Repo: siiway/serv00-daemon
Give a Star ⭐ please~
[TIP] 安装 pm2 和依赖 (python) 的耗时可能较长, 请耐心等待~
[TIP] 如遇到无法解决的问题请 Issue: https://github.com/siiway/serv00-daemon/issues/new
''')
    print('请在 Devil 控制面板 (s*.serv00.com) 创建一个 Python 项目, \n[Input] 并在此输入路径 (如 "/home/wyf9/domains/daemon.wyf9.serv00.net/"):')
    global base
    while True:
        base = input('> ')
        if os.path.exists(base):
            break
        else:
            print('目录不存在, 请重新输入 (访问 https://panel*.serv00.com/www/ 创建, * 为你的面板编号)')
    print('\nStep -1: 检查 pm2')
    if testcmd('pm2 --version'):
        print('检测到 pm2 已安装, 跳过下载')
    else:
        get_url = f'https://raw.githubusercontent.com/siiway/serv00-daemon/{branch}/script/install-pm2.sh'
        print(f'执行 pm2 --version 失败, 从 {get_url} 下载')
        get(get_url, getpth('install-pm2.sh'))
        os.system(f'bash {getpth("install-pm2.sh")}')
    print('Step 0: 安装依赖')
    install_dep_command = 'pip install flask discord-webhook pytz'
    ret = os.system(install_dep_command)
    if ret:
        raise Exception(f'安装依赖命令 {install_dep_command} 返回不为 0: {ret}')
    print('Step 1: 下载 repo')
    get(f'https://github.com/siiway/serv00-daemon/archive/refs/heads/{branch}.zip', getpth('code.zip'))
    print('Step 2: 解压代码')
    unzip('code.zip')
    print('Step 3: 拷贝文件到正确位置')
    copy(getpth(f'serv00-daemon-{branch}/app/*'), getpth('public_python/'))
    print('Step 4: 设置参数')
    configpth = getpth("public_python/config.py")
    print(f'[Tip] 可以稍后编辑 {configpth} 以修改配置.')
    file = ''
    with open(configpth, mode='r', encoding='utf-8') as f:
        file = f.read()
        f.close()
    file = user_input(name='DaemonKey', place='DaemonKey_Placeholder', desc='访问时需要携带的 key (妥善保管)', default=uuid(), file=file)
    file = user_input(name='DaemonCommand', place='DaemonCommand_Placeholder', desc='访问时需要执行的命令', default='pm2 resurrect', file=file)
    file = user_input(name='LogFile', place='LogFile_Placeholder', desc='日志文件的路径', default='/dev/null', file=file)
    print('[Tip] 配置免密登录: https://github.com/siiway/serv00-daemon?tab=readme-ov-file#ssh-免密登录')
    file = user_input(name='SSHCommand', place='SSHCommand_Placeholder', desc='ssh 连接命令, 如不想创建公钥可以使用 sshpass, 否则默认即可', default='ssh localhost "devil info account"', file=file)
    file = user_input(name='WebhookUrl', place='WebhookUrl_Placeholder', desc='Discord 的 Webhook URL (在 编辑频道 > 整合 > Webhook 创建), 为空禁用推送', default='', file=file)
    file = user_input(name='Timezone', place='Timezone_Placeholder', desc='消息中显示时间的时区', default='Asia/Shanghai')
    with open(configpth, mode='w', encoding='utf-8') as f:
        f.write(file)
        f.close()


if __name__ == '__main__':
    main()
    print('安装成功!')
    print('Visit: https://github.com/siiway/serv00-daemon?tab=readme-ov-file#继续')
    print()
