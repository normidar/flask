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