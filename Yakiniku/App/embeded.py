from PIL import Image, ImageDraw, ImageFont, ImageFilter
import infostruct as ifs

rotateWords = '`·~!@#$%^…&*()（）-=[]【】\\;\'‘’「」\"“”『』.,/_—+{}|:”<>《》?0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '


def DrawWord(image, word, position, direction, fontName, fontSize, fontColor='#000000', bold=False):
    font = ImageFont.truetype(fontName, fontSize)
    if direction == 1 and rotateWords.find(word) >= 0:
        w = Image.new(mode='RGB', size=(fontSize, fontSize), color="#FFFFFF")
        ImageDraw.Draw(w).text((0, 0), word, font=font, fill=fontColor)
        if bold:
            ImageDraw.Draw(w).text((0, -1), word, font=font, fill=fontColor)
        image.paste(w.rotate(270), position)
    else:
        width = font.getsize(word)[0]
        # print(word + str(width))
        position = (position[0] + (fontSize - width) // 2, position[1]) if direction == 1 else position
        ImageDraw.Draw(image).text(position, word, font=font, fill=fontColor)
        if bold:
            ImageDraw.Draw(image).text((position[0] + 1, position[1]), word, font=font, fill=fontColor)


def DrawText(image, text, startPoint, direction, maxLength, fontName, fontSize, fontColor='#000000', bold=False, tracking=0, spacing=0):
    font = ImageFont.truetype(fontName, fontSize)
    p = (startPoint[0] - fontSize, startPoint[1]) if direction == 1 else startPoint
    for c in text:
        cSize = fontSize if direction == 1 and rotateWords.find(c) < 0 else font.getsize(c)[0]
        if c == '\n':
            p = (p[0] - fontSize - spacing, startPoint[1]) if direction == 1 else (startPoint[0], p[1] + fontSize + spacing)
            continue
        if p[direction] + cSize > startPoint[direction] + maxLength:
            p = (p[0] - fontSize - spacing, startPoint[1]) if direction == 1 else (startPoint[0], p[1] + fontSize + spacing)
        DrawWord(image=image, word=c, position=p, direction=direction, fontName=fontName, fontSize=fontSize, fontColor=fontColor, bold=bold)
        p = (p[0], p[1] + cSize + tracking) if direction == 1 else (p[0] + cSize + tracking, p[1])


def GetRow(text, maxLength, direction, fontName, fontSize, tracking=0):
    font = ImageFont.truetype(fontName, fontSize)
    row = 1
    pos = 0
    for c in text:
        cSize = fontSize if direction == 1 and rotateWords.find(c) < 0 else font.getsize(c)[0]
        if c == '\n':
            row += 1
            pos = 0
            continue
        if pos + cSize > maxLength:
            row += 1
            pos = 0
        pos += cSize + tracking
    return row


def GetTracking(text, maxLength, direction, fontName, fontSize):
    font = ImageFont.truetype(fontName, fontSize)
    cnt = 0
    pos = 0
    tracking = int(fontSize * 0.07)
    for c in text:
        cSize = fontSize if direction == 1 and rotateWords.find(c) < 0 else font.getsize(c)[0]
        if c == '\n':
            tracking = min(tracking, tracking if cnt <= 1 else (maxLength - pos) // (cnt - 1))
            cnt = 0
            pos = 0
            continue
        if pos + cSize > maxLength:
            tracking = min(tracking, tracking if cnt <= 1 else (maxLength - pos) // (cnt - 1))
            cnt = 0
            pos = 0
        cnt += 1
        pos += cSize
    tracking = min(tracking, tracking if cnt <= 1 else (maxLength - pos) // (cnt - 1))
    return tracking


def DrawRect(image, text, p1, p2, direction, fontName, fontColor='#000000', bold=False):
    width = p2[0] - p1[0] if direction == 1 else p2[1] - p1[1]
    length = p2[1] - p1[1] if direction == 1 else p2[0] - p1[0]

    fontSize = 60
    tracking = 0
    spacing = fontSize // 5

    for i in range(0, 60):
        row = GetRow(text=text, maxLength=length, direction=direction, fontName=fontName, fontSize=fontSize)
        if row * fontSize + (row - 1) * spacing <= width:
            break
        else:
            fontSize -= 1
            spacing = fontSize // 5
    tracking = GetTracking(text=text, maxLength=length, direction=direction, fontName=fontName, fontSize=fontSize)
    if direction == 1:
        p2 = (p2[0] - (width - row * fontSize - (row - 1) * spacing) // 2, p2[1])
    else:
        p1 = (p1[0], p1[1] + (width - row * fontSize - (row - 1) * spacing) // 2)
    DrawText(image=image, text=text, startPoint=(p2[0], p1[1]) if direction == 1 else p1, maxLength=length, direction=direction, fontName=fontName, fontSize=fontSize, fontColor=fontColor, bold=bold, tracking=tracking, spacing=spacing)


def DrawPoly(image, text, points, direction, fontName, fontColor='#000000', bold=False):
    ImageDraw.Draw(image).polygon(xy=points, fill='#FFFFFF')
    _p1 = _p2 = points[0]
    for p in points:
        _p1 = (min(_p1[0], p[0]), min(_p1[1], p[1]))
        _p2 = (max(_p2[0], p[0]), max(_p2[1], p[1]))
    DrawRect(image=image, text=text, direction=direction, p1=_p1, p2=_p2, fontName=fontName, fontColor=fontColor, bold=bold)


def Embeded(file, outname, infos):
    image = Image.open(file)
    fontName = 'simhei.ttf'
    for item in infos:
        if (item.enable != 1):
            continue
        points = []
        for po in item.vertexs:
            points.append((po[0], po[1]))
        DrawPoly(image=image, text=item.trans, points=points, direction=item.direct, fontName=fontName)
    image.save(outname)


if __name__ == '__main__':
    infos = []

    bound = [[405, 103], [405, 278], [285, 278], [285, 103]]
    text = '暑假已经快要结束了……'
    info = ifs.Info(bound, 1, text, text)
    infos.append(info)

    bound = [[1010, 575], [1010, 732], [1091, 732], [1091, 575]]
    text = '脚本似乎还能做得完？'
    info = ifs.Info(bound, 1, text, text)
    infos.append(info)

    bound = [[1254, 1352], [1254, 1487], [1180, 1487], [1180, 1352]]
    text = '要做些什么……'
    info = ifs.Info(bound, 1, text, text)
    infos.append(info)

    Embeded('t.png', 't_out.png', infos)

'''
fontName = 'simhei.ttf'

image = Image.open("t.png")
DrawPoly(image=image, text='暑假已经快要结束了……', points=[(405, 103), (405, 278), (285, 278), (285, 103)], direction=1, fontName=fontName)
DrawPoly(image=image, text='脚本似乎还能做得完？', points=[(1010, 575), (1010, 732), (1091, 732), (1091, 575)], direction=1, fontName=fontName)
DrawPoly(image=image, text='要做些什么……', points=[(1254, 1352), (1254, 1487), (1180, 1487), (1180, 1352)], direction=1, fontName=fontName)
DrawPoly(image=image, text='你还好吗…？', points=[(899, 1433), (899, 1616), (836, 1616), (836, 1433)], direction=1, fontName=fontName)
DrawPoly(image=image, text='明天我可以去你家吗？', points=[(789, 1593), (789, 1733), (676, 1733), (676, 1593)], direction=1, fontName=fontName)
DrawPoly(image=image, text='让学生会的节目更加有趣——下定决心的历开始兴奋起来但……？', points=[(1345, 399), (1345, 1917), (1297, 1917), (1297, 399)], direction=1, fontName=fontName, bold=True)
image.save('t_translated.png')
# image.show()

image = Image.open("1.jpg")
draw = ImageDraw.Draw(image)
DrawPoly(image=image, text='那个时候', points=[(895, 102), (916, 101), (922, 228), (901, 229)], direction=1, fontName=fontName)
DrawPoly(image=image, text='确实，在春天，我开始喜欢这里的武士', points=[(744, 232), (862, 229), (866, 403), (748, 406)], direction=1, fontName=fontName)
DrawPoly(image=image, text='因为我说我不喜欢别人', points=[(143, 447), (246, 445), (251, 640), (148, 642)], direction=1, fontName=fontName)
image.save('1_translated.jpg')

image = Image.open("2.png")
draw = ImageDraw.Draw(image)
DrawPoly(image=image, text='Hayashi Hayashi\n教授', points=[(1169, 369), (1387, 384), (1383, 446), (1165, 431)], direction=0, fontName=fontName, bold=True)
DrawPoly(image=image, text='新产品发布纪念签名会', points=[(1187, 444), (1388, 444), (1388, 533), (1187, 533)], direction=0, fontName=fontName, bold=True)
DrawPoly(image=image, text='6F特殊场地00开放30', points=[(1189, 560), (1420, 560), (1420, 638), (1189, 638)], direction=0, fontName=fontName, bold=True)
DrawPoly(image=image, text='我可以见到老师', points=[(1059, 1092), (1147, 1092), (1147, 1230), (1059, 1230)], direction=1, fontName=fontName)
DrawPoly(image=image, text='当然，老师写的是一本小说', points=[(1078, 1573), (1203, 1567), (1213, 1764), (1088, 1770)], direction=1, fontName=fontName)
DrawPoly(image=image, text='我毫无例外地阅读了所有的文章和访谈', points=[(880, 1620), (1025, 1620), (1025, 1829), (880, 1829)], direction=1, fontName=fontName)
DrawPoly(image=image, text='我来了', points=[(744, 424), (780, 424), (780, 573), (744, 573)], direction=1, fontName=fontName)
DrawPoly(image=image, text='OOKS', points=[(333, 372), (615, 372), (615, 436), (333, 436)], direction=0, fontName=fontName)
DrawPoly(image=image, text='危险', points=[(351, 1255), (382, 1255), (382, 1344), (351, 1344)], direction=1, fontName=fontName)
DrawPoly(image=image, text='因为老师在陪审团里，我把我的小说放在新人奖中', points=[(172, 1587), (327, 1587), (327, 1824), (172, 1824)], direction=1, fontName=fontName)
image.save('2_translated.png')
'''
