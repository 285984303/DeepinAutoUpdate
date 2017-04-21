# /home/adinlead/Project/PyProject/DeepinAutoUpdate/stopproc.sh autoUpdateWallpaperMain.sh

# 先定位到运行目录(如果目录不同请修改此处)
cd /home/adinlead/Project/PyProject/DeepinAutoUpdate/src/

while true
do
    # 运行脚本
    python Main.py
    #获得当前时间
    ls_date=`date '+%Y-%m-%d %H:%M:%S'`
    time_text="UPDATE TIME:"
    # 打印当前时间
    echo time_text ${ls_date}
    # 记录当前时间
    echo ${ls_date} >> /tmp/auw/dau.log
    # 等5分钟(如果想修改更新频率请修改此处)
    sleep 5m
done