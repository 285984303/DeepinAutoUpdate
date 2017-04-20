# -*-coding:utf-8-*-
import commands
import json
import os

import time
import urllib2
import ImageTools

import sys
import Setting

reload(sys)
sys.setdefaultencoding('utf8')

if not os.path.isdir('/tmp/auw/'):
    os.mkdir('/tmp/auw/')


def main():
    # 读取配置文件的信息

    citycode = Setting.city
    if len(sys.argv) == 1 or len(sys.argv[1]) == 0:
        wallpath = Setting.wallpath
    else:
        wallpath = sys.argv[1]
        config = "# -*-coding:utf-8-*-\ncity = '%s'\nwallpath = '%s'" % (citycode, wallpath)
        config_file = open('Setting.py', 'w')
        config_file.write(config)
        config_file.close()

    # 设置请求地址与请求参数
    request_url = 'http://d1.weather.com.cn/sk_2d/%s.html?_=%s' % (citycode, int(round(time.time() * 1000)))

    request = urllib2.Request(request_url)
    request.add_header('referer', 'http://www.weather.com.cn/weather1d/101120101.shtml')
    response = urllib2.urlopen(request)

    # 读取请求结果并转换为JSON
    result = response.read()
    result = result.replace('var dataSK = ', '')
    result = json.loads(result)

    watermark = ImageTools.toWatermarkImage(result)

    new_wallpath = ImageTools.brand(wallpath, watermark)

    commands.getstatusoutput("gsettings set org.gnome.desktop.background picture-uri %s" % new_wallpath)


if __name__ == __name__:
    main()
