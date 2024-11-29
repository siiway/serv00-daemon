# serv00-daemon

基于 Python WWW Pages 的 Serv00 Daemon, 实现进程保活/自动保号

(正在加急开发)

## 功能

1. 自动拉起 Serv00 进程
2. 

## 准备工作

如果没有 PM2, 则用下面的脚本安装:

```bash
# 从 GitHub 下载脚本 (本 repo 的 /pm2/install-pm2.sh)
bash <(curl -s https://raw.githubusercontent.com/siiway/serv00-daemon/main/script/install-pm2.sh)

# 测试安装:
pm2 --version
# 如正常, 应显示版本号如 5.4.3
```

## 安装

```shell
wget -O install-daemon.py https://raw.githubusercontent.com/siiway/serv00-daemon/main/script/install-daemon.py && python3 install-daemon.py && rm install-daemon.py
```

> 不会自动安装 pm2

## 继续

