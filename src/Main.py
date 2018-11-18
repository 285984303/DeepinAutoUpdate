# -*-coding:utf-8-*-
import commands
import json
import os

import time
import urllib2
import ImageTools

import sys
import Setting
import DownBingWallpaper

reload(sys)
sys.setdefaultencoding('utf8')

if not os.path.isdir('/tmp/auw/'):
    os.mkdir('/tmp/auw/')


def main():
    # 读取配置文件的信息

    citycode = Setting.city

    if Setting.downwall:
        wallpath = '/tmp/auw/bing_wall.jpg'
    else:
        if len(sys.argv) == 1 or len(sys.argv[1]) == 0:
            wallpath = Setting.wallpath
            print wallpath
        else:
            wallpath = sys.argv[1]
            config = "# -*-coding:utf-8-*-\n" \
                     "# 城市代码\n" \
                     "city = '%s'\n" \
                     "# 是否下载网络壁纸\n" \
                     "downwall=%s\n" \
                     "# 本地壁纸路径\n" \
                     "wallpath = '%s'" \
                     % (citycode, 'False', wallpath)

            config_file = open('Setting.py', 'w')
            config_file.write(config)
            config_file.close()

    # 设置请求地址与请求参数
    #request_url = 'http://d1.weather.com.cn/sk_2d/%s.html?_=%s' % (citycode, int(round(time.time() * 1000)))
    #request_url = 'http://mobile.weather.com.cn/data/sk/%s.html?_=%s' % (citycode, int(round(time.time() * 1000)))
    request_url = 'http://api.help.bj.cn/apis/weather6d/?id=%s&_=%s' % (citycode, int(round(time.time() * 1000)))
    #request_url = 'http://www.weather.com.cn/data/sk/%s.html?_=%s' % (citycode, int(round(time.time() * 1000)))

    request = urllib2.Request(request_url)
    #request.add_header('referer', 'http://www.weather.com.cn/weather1d/101120101.shtml')
    request.add_header('referer', 'http://www.weather.com.cn/data/sk/101010100.html')
    response = urllib2.urlopen(request)

    # 读取请求结果并转换为JSON
    result = response.read()
    #result = result.replace('var dataSK = ', '')
    print(result)
    #result = result.replace('var hour3data=', '')
    result = json.loads(result)
    #print(result)
    watermark = ImageTools.toWatermarkImage(result)

    # 在必应下载壁纸
    if Setting.downwall:
        DownBingWallpaper.downNow(wallpath)
    ImageTools.changeSize(wallpath)
    new_wallpath = ImageTools.brand(wallpath, watermark)
    print new_wallpath
    #commands.getstatusoutput("gsettings set org.gnome.desktop.background picture-uri %s" % new_wallpath)
    commands.getstatusoutput("gsettings set com.deepin.wrap.gnome.desktop.background picture-uri %s" % new_wallpath)
    #commands.getstatusoutput('qdbus --literal com.deepin.wm /com/deepin/wm com.deepin.wm.SetTransientBackground "file://%s"' % new_wallpath)

if __name__ == __name__:
    main()
