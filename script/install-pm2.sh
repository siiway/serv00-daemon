# Original From: https://github.com/k0baya/alist_repl/blob/main/serv00/install-pm2.sh
read -p "确定安装 pm2? (Enter: 确认/^C: 取消)" ctn
echo "开始安装..."
echo
echo "---"
mkdir -p ~/.npm-global && npm config set prefix '~/.npm-global' && echo 'export PATH=~/.npm-global/bin:$PATH' >>~/.profile && source ~/.profile && npm install -g pm2 && source ~/.profile
echo "---"
echo
echo "pm2 成功安装，断开 SSH 连接后重连生效。请不要删除或覆盖 ~/.profile 配置文件"
echo
echo "形如 npm error config prefix cannot be changed from project config 的日志不会影响 pm2 的使用，请无需在意。"
echo
echo "抄袭且不标注出处可耻！"
echo
echo "请认准原作者：https://saika.us.kg/"
echo
echo "--- used by https://github.com/siiway/serv00-daemon"
echo "0. 虽然但是，我也不知道原作者 Saika 为什么要加一个 base64 encrypt (防君子不防小人? 或是防等级低的小人)"
echo "1. 首先我不是小人 ↓"
echo "2. ↑ 贴上代码 blob: https://github.com/k0baya/alist_repl/blob/main/serv00/install-pm2.sh"
echo "3. 整了大半天还是搞不明白为什么 base64 解出来是 PATH 变量名, 但下载执行就变成了自己服务器的 PATH, 所以---我决定不用 base64 了 :( -- wyf9"
echo