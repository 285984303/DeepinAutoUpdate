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
    i = Image.new("RGBA", (290, 150), (255, 255, 255, 120))
    d = ImageDraw.Draw(i)

    # 输出城市信息
    d.text((20, 0), result['cityname'].decode('UTF8'), font=ImageFont.truetype("font.ttf", 72), fill=textcolor)

    d.text((len(result['cityname']) * 72 + 26, 72 - 48), result['temp'].decode('UTF8'),
           font=ImageFont.truetype("font.ttf", 48), fill=textcolor)
    d.text((len(result['cityname']) * 72 + len(result['temp']) * 48 - 12, 72 - 32), "℃".decode("UTF8"),
           font=ImageFont.truetype("font.ttf", 32), fill=textcolor)

    d.line(((20, 85), (270, 85)), (0, 0, 0), width=2)

    msg = "%(weather)s | %(WD)s %(WS)s %(wse)s" % result
    d.text((20, 90), msg.decode('UTF8'), font=ImageFont.truetype("font.ttf", 20), fill=textcolor)

    msg = "湿度:%(SD)s | %(WRDJ)s" % result

    d.text((20, 115), msg.decode('UTF8'), font=ImageFont.truetype("font.ttf", 20), fill=textcolor)

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
