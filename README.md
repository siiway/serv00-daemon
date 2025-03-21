# serv00-daemon

<!--
> 来投个票? `>` **[discussion#3](https://github.com/siiway/serv00-daemon/discussions/3)** `<` <br/>
> ~~放整整一个月了没人投票，哇啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊 😭😭😭~~
我已经不指望有人投了，就这样吧
-->

基于 Python WWW Pages 的 Serv00 Daemon, 实现进程保活/自动保号

## 手把手教程

如果觉得看不懂，可以参考 [我在 Linux DO 站发布的帖子](https://linux.do/t/topic/491153?u=wyf9)

有详细的部署教程和配图，更建议小白阅读~

## 功能

1. 自动拉起在 PM2 上托管的进程
2. 使用 SSH 登录的方式自动保活 (续期)

## Why this project?

> [!WARNING]
> *声明: 这一段(甚至大部分readme)都是在凌晨写的 (不信看 [commit (24-11-30)](https://github.com/siiway/serv00-daemon/commit/fbe465b0d7faefbaa0bfa1e5dd2dcd6f954ef6bd) 和 [commit (24-12-01)](https://github.com/siiway/serv00-daemon/commit/d85171835d49f83575afd71dff4813ee06bb4d7b)), 部分内容**可能有争议/错误**, 请勿开骂qwq*

Serv00 自动续期有两种方案:

1. [ ] 通过 s*.serv00.com 登录面板 ([已有人实现](https://github.com/lopins/serv00-auto-scripts))
2. [x] **通过 SSH 登录命令行 ([亦已有人实现](https://github.com/bin862324915/serv00-automation))** 用的是这个 ~~(思路! 思路!)~~

那你*可能*就要替我想了：为什么还要做这个项目? 直接用现成的不得了?

1. 首! 先! github actions 不是一个很好的方案, 在于一段时间没推送到这个 repo 就会禁用定时 trigger (而且还不会通知你)
2. 其! 次! 这个项目将两个功能整合到了一起; 还有自动脚本, 省去部署的麻烦
3. 还! 有! 本项目的进程保活通过访问 url 实现, 非常稳定 (个人 s7/s9/s14 自测), 拉起间隔完全取决于你自己 (UptimeRobot 免费版最短 5 min, cron-job 最短 1 min)
3.5. 因为使用 Serv00 面板自带的网站功能, 可以保证本 Daemon 的自启而不会被杀掉, 更加稳定
4. 最! 后! 本项目自动登录的推送功能单独拆分为一个文件, 方便修改; ~~内置 Discord 推送, 使用卡片渲染更加美观！~~
5. 好吧编不出来了( ~~总之用它就对了!~~

本项目使用 pm2 作为进程管理工具，在使用前请先了解 [pm2 的基本使用方法](https://www.cnblogs.com/chyingp/p/pm2-documentation.html) 或自行搜索需要的用法 (很简单)

### SSH 免密登录

一行命令:
```shell
mkdir -p ~/.ssh && cd ~/.ssh && ssh-keygen -t rsa && cat id_rsa.pub >> authorized_keys
```

> [!IMPORTANT]
> 在 `ssh-keygen` 生成密钥时请直接回车 *(不要多)* 使用默认值，**不要**更改默认保存位置，且请使用**空密码**以便直接连接

<details>
<summary>这行命令会做什么</summary>

```shell
# -1. 创建 ~/.ssh 目录 *(如有则忽略)*
mkdir -p ~/.ssh

# 0. 切目录到 ~/.ssh
cd ~/.ssh

# 1. 先检查有没有 id_rsa 和 id_rsa.pub
# *如果有可以直接跳过第 2 步*
ls -l

# 2. 如果没有: 生成一个新的密钥
# 建议*一路回车*, 直接不带密码保存到默认目录即可 **(必须不带密码)**
ssh-keygen -t rsa

# 3. 追加**公钥**到信任列表 (分清楚: 公钥带 `.pub` 后缀, 内容**较短**; 私钥没有, 内容**较长**, 且有如 `-----BEGIN OPENSSH PRIVATE KEY-----` 之类的标志)
# 一定用两个 >, 否则会把其他的清了!
cat id_rsa.pub >> authorized_keys

# 4. 测试效果
ssh localhost
```

</details>

## 安装

```shell
wget -O install-daemon.py https://raw.githubusercontent.com/siiway/serv00-daemon/main/script/install-daemon.py && python3 install-daemon.py && rm install-daemon.py
```

> 如果没有安装 pm2 会自动下载[脚本](https://github.com/siiway/serv00-daemon/blob/main/script/install-pm2.sh)并安装.

在安装过程中会询问下面的信息 *(不填回车就是默认)*:

- DaemonKey (`访问时需要携带的 key (妥善保管)`): 其实就是类似于密钥一类的东西, 默认随机生成一个[uuid](https://www.bing.com/search?q=uuid)
- DaemonCommand (`访问时需要执行的命令`): ← 在 pm2 中为 `pm2 resurrect`, 也是本项默认值
  * 这个命令不太清楚, 但能用就行 (如果pm2没启动就会恢复进程，启动了什么都不做)
  * 使用pm2记得作更改后用 `pm2 save` 保存到 dump 文件，否则重启会丢失!
- LogFile (`日志文件的路径`): 也是顾名思义, 默认是 `/dev/null`, 即不保存日志
- SSHCommand (`ssh 连接命令, 如不想创建公钥可以使用 sshpass, 否则默认即可`): ← 不想创建公钥可以用 `sshpass -p "你的密码" ssh localhost "devil info account"`
- WebhookUrl (`Discord 的 Webhook URL (在 编辑频道 > 整合 > Webhook 创建), 为空禁用推送`): ← 我自认为我已经说得很清楚了
- Timezone (`消息中显示时间的时区`): 类似 [`Asia/Shanghai`](https://www.bing.com/search?q=Asia%2FShanghai) 的时区字符串, 在处理 Webhook 消息时会将时间转换到目标时区

> [!NOTE]
> 如果报错找不到库, 请手动安装: `pip install flask requests`

## 继续

使用 [上一步](#安装) 的脚本安装完成后, 链接会将你带到这里, 接下来我们就要进行简单的收尾工作: **接入定时器** 了.

虽然简单, 但这也是**最重要**的一步, 它决定了你的 Daemon 如何定时触发

> [!IMPORTANT]
> 继续之前, 在你的 Devil 控制面板重启网站. <br/>
> 在这里我使用 [UptimeRobot](https://dashboard.uptimerobot.com/) 作演示, 也可选择其他类似的 url 监测平台 <br/>
> 其实更推荐 cron-job.org, 全免费, 且相比 UptimeRobot 限制更少 (上面提到的 Linux DO 帖子中就使用了 cron-job.org 作演示)

### urls

```md
**!这里需要创建两个监视器!**

- 1) pm2 进程保活 (建议设置 5 分钟)
  * http://USERNAME.serv00.net/daemon/MyKey

- 2) 登录 SSH 保号 (建议设置一天至一月不等)
  * http://USERNAME.serv00.net/renew/MyKey

替换以下字段:
- http: 协议, 如果直接使用 用户名.serv00.net 可使用 https; 如使用类似 xxx.用户名.serv00.net 的子域名默认只能使用 http
- USERNAME.serv00.net: 部署的域名
- MyKey: 前面设置的密钥
```

### UptimeRobot

1. 注册, 登录
2. 创建一个 `Single monitor`

![continue-2](./img/continue-2.png)

1. 选择监测类型为 `HTTP / website monitoring`, 填写 url, 并选择 `Monitor interval` (最快 5 min 请求一次), 保存即可.

![continue-3](img/continue-3.png)

> [!TIP]
> 可以直接访问拼接的 url 测试是否能使用, 如果配置正确, 应该会显示类似下图的内容:

![continue-test](img/continue-test.png)

~~漏token了? 你说得很对, 但是已经被我重置了~~

也可以使用 [cron-job](https://console.cron-job.org/) 监视, 照填即可↓

![continue-cronjob-org](img/continue-cronjob-org.png)

## End

如果对此项目有建议/想法，可 [Issue](https://github.com/siiway/serv00-daemon/issues/new) 或 [More contact](https://wyf9.top/#/contact).

在此推荐一篇 Serv00 应用部署教程 (上面pm2安装脚本作者的文章): https://saika.us.kg/2024/01/27/serv00_logs/

这个是搬运不带原文链接的，建议看评论 → https://bs.openface.cc/2024/06/serv00.html [[Archive (25-01-14)](https://web.archive.org/web/20250114132932/https://bs.openface.cc/2024/06/serv00.html)]

https://github.com/siiway/serv00-daemon/blob/d5359bf9d12d8758b8bb0ccb55610d23691e1233/script/install-pm2.sh#L13

本项目使用 **MIT** 作为 [LICENSE](./LICENSE).
