
状态码
201 成功创建资源
202 异步代码处理中,请稍后再次拉取
204 没有需要返回的数据

400 未知错误
401 未放token
402 未支付
403 权限不足
404 找不到页面
422 传值不正确
423 资源被锁
501 目前未实现的API





----------------------------------------------------------------

nohup python3 run.py >> /www/wwwroot/log/flask.log 2>&1 &

source my_env/bin/activate

pip3 install -r requirements.txt

//安装screen请使用apt:
apt-get update
apt-get install screen

screen -S name  //创建 名为name的 screen
screen -ls  //列出所有screen
screen -d -r [pid(名字前的数字)]  //进入screen tt


> ctrl a d 退出screen
> exit 关闭screen窗口

# git 强制更新
git fetch --all
git reset --hard origin/master