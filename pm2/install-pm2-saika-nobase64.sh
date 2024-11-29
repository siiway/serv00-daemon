# From: https://github.com/k0baya/alist_repl/blob/main/serv00/install-pm2.sh
mkdir -p ~/.npm-global && npm config set prefix '~/.npm-global' && echo 'export PATH=~/.npm-global/bin:$PATH' >>~/.profile && source ~/.profile && npm install -g pm2 && source ~/.profile
clear
echo "pm2 成功安装，断开 SSH 连接后重连生效。请不要删除或覆盖 ~/.profile 配置文件"
echo
echo
echo
echo "形如 npm error config prefix cannot be changed from project config 的日志不会影响 pm2 的使用，请无需在意。"
echo
echo
echo
echo "抄袭且不标注出处可耻！"
echo
echo
echo
echo "请认准原作者：https://saika.us.kg/"