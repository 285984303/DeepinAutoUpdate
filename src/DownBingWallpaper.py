# -*-coding:utf-8-*-
import commands
import random
import urllib
import urllib2
from bs4 import BeautifulSoup


def downNow(img_save):
    page = random.randint(1, 35)
    # page = 1

    url = 'https://bing.ioliu.cn/?p=%s' % page
    # 设置请求地址与请求参数

    request = urllib2.Request(url=url)
    # request.add_header('referer', 'http://www.weather.com.cn/weather1d/101120101.shtml')
    response = urllib2.urlopen(request)
    # 读取请求结果并转换为JSON
    result = response.read()
    html = BeautifulSoup(result, 'lxml')
    html = html.select('.container')[1]
    html = html.select('.mark')
    html = html[random.randint(0, len(html) - 1)]
    img_name = html.get('href')
    img_name = img_name.replace('/photo/', '')
    img_name = img_name[:img_name.rfind('?')]
    img_href = 'https://static.ioliu.cn/bing/%s_1920x1080.jpg' % img_name

    # 下载图片
    comm = 'wget %s -O %s' % (img_href, img_save)
    commands.getstatusoutput(comm)
    return img_save
