# coding: utf-8
# config.py: 一些配置

# 访问 key, 请妥善保管
DAEMON_KEY = 'DaemonKey_Placeholder'
# 启动命令
DAEMON_COMMAND = 'DaemonCommand_Placeholder'
# 日志文件目录
LOG_FILE = 'LogFile_Placeholder'
# ssh 连接命令, 如不想[创建公钥](https://github.com/siiway/serv00-daemon/tree/main?tab=readme-ov-file#ssh-免密登录) 可以在命令前添加: sshpass -p "你的密码"
SSH_COMMAND = 'SSHCommand_Placeholder'
# Discord Webhook URL
WEBHOOK_URL = 'WebhookUrl_Placeholder'
# Webhook 推送时所有时间的时区, `洲/城市` (自行搜索 pytz 库用法), 一般用 `Asia/Shanghai` (北京时间) 或 `UTC` (即 +0, 北京时间 - 8)
TIMEZONE = 'Timezone_Placeholder'