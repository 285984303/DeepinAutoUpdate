# /home/adinlead/Project/PyProject/DeepinAutoUpdate/stopproc.sh autoUpdateWallpaperMain.sh

while true
do
    # 先定位到运行目录
    cd /home/adinlead/Project/PyProject/DeepinAutoUpdate/src/
    # 运行脚本
    python Main.py
    #获得当前时间
    ls_date=`date '+%Y-%m-%d %H:%M:%S'`
    time_text="UPDATE TIME:"
    # 打印当前时间
    echo time_text ${ls_date}
    # 记录当前时间
    echo ${ls_date} >> /tmp/auw/dau.log
    # 等5分钟
    sleep 5m
done