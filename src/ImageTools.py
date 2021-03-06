# -*-coding:utf-8-*-
import os
import shutil
from PIL import Image, ImageDraw, ImageFont


def getPollutionLevel(lev):
    lev = int(lev)

    if lev < 51:
        return '%s 优' % lev
    elif lev < 101:
        return '%s 良' % lev
    elif lev < 151:
        return '%s 轻度污染' % lev
    elif lev < 201:
        return '%s 中度污染' % lev
    elif lev < 301:
        return '%s 重度污染' % lev
    else:
        return '%s 严重污染' % lev


def toWatermarkImage(result):
    # Configurations:
    textcolor = "#000000"

    # Build rich text for ads
    ad = []

    # Wrap line for text
    #   Special treated Chinese characters
    #   Workaround By Felix Yan - 20110508
    wraptext = [""]

    result['WRDJ'] = getPollutionLevel(result['aqi'])
    result['wse'] = result['wse'].replace('&lt;', '')

    # Format wrapped lines to rich text
    wrap = [(text, textcolor) for text in wraptext]
    wrap += ad

    # Draw picture
    i = Image.new("RGBA", (290, 158), (255, 255, 255, 120))
    d = ImageDraw.Draw(i)
    # 输出城市信息
    d.text((20, 0), result['cityname'].decode('UTF8'), font=ImageFont.truetype("font.ttf", 72), fill=textcolor)
    # 输出温度信息
    d.text((len(result['cityname']) * 72 + 26, 72 - 48), ('%s℃' % result['temp']).decode('UTF8'),
           font=ImageFont.truetype("font.ttf", 48), fill=textcolor)
    # 添加分隔线
    d.line(((10, 82), (280, 82)), (0, 0, 0), width=3)
    # 添加天气和风力信息
    msg = "%(weather)s | %(WD)s %(WS)s %(wse)s" % result
    d.text((20, 88), msg.decode('UTF8'), font=ImageFont.truetype("font.ttf", 20), fill=textcolor)
    # 添加湿度和空气质量信息
    msg = "湿度:%(SD)s | %(WRDJ)s" % result
    d.text((20, 111), msg.decode('UTF8'), font=ImageFont.truetype("font.ttf", 20), fill=textcolor)
    # 添加一个灰色底色 用于衬托更新时间
    d.line(((0, 146), (290, 146)), (220, 220, 220, 220), width=24)

    # 输出更新时间信息
    d.text((20, 135), u'%s %s | 更新' % (result['date'].decode("UTF8"), result['time'].decode("UTF8")),
           font=ImageFont.truetype("font.ttf", 17), fill="#000000")

    # Write result to a temp file
    filename = "/tmp/auw/watermark.png"
    with open(filename, "wb") as s:
        i.save(s, "PNG")
    return filename


def brand(wallpath, watermark):
    new_wallpath = '/tmp/auw/wallpaper%s' % wallpath[wallpath.rfind('.'):]
    shutil.copy(wallpath, new_wallpath)

    im = Image.open(new_wallpath)
    mark = Image.open(watermark)
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    layer.paste(mark, (im.size[0] - mark.size[0], mark.size[1]))
    out = Image.composite(layer, im, layer)
    out.save(new_wallpath)
    return new_wallpath
