from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
import os
import sys
import time
import datetime
import random
from PIL import Image
from django.conf import settings
from . import yakimain as yaki
from . import infostruct as ifs


def runmain(name, diction):
    print('Processing ' + name + ' ... ')
    print(settings.UPLOAD_ROOT)
    print(settings.RESULT_ROOT)
    ret = yaki.doall(settings.UPLOAD_ROOT + '/' + name, settings.RESULT_ROOT + '/s_' + name, settings.RESULT_ROOT + '/' + name, diction)
    return ret


def cleanf():
    pathup = settings.UPLOAD_ROOT
    pathdo = settings.RESULT_ROOT
    dirs = os.listdir(pathup)
    for file in dirs:
        if (time.time() - os.path.getatime(os.path.join('upload', file)) > 8 * 60 * 60):
            os.remove(os.path.join('upload', file))
    dirs = os.listdir(pathdo)
    for file in dirs:
        if (time.time() - os.path.getatime(os.path.join('result', file)) > 8 * 60 * 60):
            os.remove(os.path.join('result', file))


def upload(request):
    cleanf()
    if request.method == 'GET':
        t = random.randint(1, 4)
        return render(request, 'upload.html', {'images': t, 'alert': 'false'})
    elif request.method == 'POST':
        obj = request.FILES.get('pic')
        if obj == None:
            t = random.randint(1, 4)
            return render(request, 'upload.html', {'images': t, 'alert': 'false'})

        fix = random.randint(0, 99999)
        f = open(os.path.join('upload', str(fix) + obj.name), 'wb')
        for line in obj.chunks():
            f.write(line)
        f.close()

        try:
            img = Image.open(os.path.join('upload', str(fix) + obj.name))
            # print("图像格式", img.format)
        except:
            t = random.randint(1, 4)
            return render(request, 'upload.html', {'images': t, 'alert': 'true'})

        if (img.format == 'TIFF'):
            t = random.randint(1, 4)
            return render(request, 'upload.html', {'images': t, 'alert': 'true'})

        #diction = [['侑', '侑']]
        diction = []
        concat = request.POST
        # print(concat)
        for i in range(0, 10):
            key1 = "name" + str(i)
            key2 = "trans" + str(i)
            if concat[key1] == '':
                continue
            if concat[key2] == '':
                continue
            diction.append([concat[key1], concat[key2]])

        print(diction)

        ret = runmain(str(fix) + obj.name, diction)
        for item in ret:
            item.user = item.trans

        request.session['infos'] = ret
        request.session['picname'] = str(fix) + obj.name
        request.session['oriname'] = obj.name
        request.session['size'] = [img.size[0], img.size[1]]

        return HttpResponseRedirect('show.html')
        # return show(request, obj.name)
        # return HttpResponse(obj.name)


def show(request):
    cleanf()
    picname = request.session.get('picname')
    oriname = request.session.get('oriname')
    infos = request.session.get('infos')
    size = request.session.get('size')
    print(picname)
    if request.method == 'GET':
        return render(request, 'show.html', {'images': picname, 'infos': infos, 'oriname': oriname})
    elif request.method == 'POST':
        concat = request.POST
        print(concat)
        print(concat.getlist('enable'))
        # print(concat['newone'])
        print(len(infos))
        eabs = concat.getlist('enable')
        for info in infos:
            info.enable = 0
        for item in eabs:
            pid = int(item)
            if pid < len(infos):
                infos[pid].enable = 1
        for info in infos:
            key = "trans" + str(info.id)
            info.user = concat[key]
            key = "bold" + str(info.id)
            if len(concat.getlist(key)):
                info.bold = True
            else:
                info.bold = False
            key = "dire" + str(info.id)
            if len(concat.getlist(key)):
                info.direct = 0
            else:
                info.direct = 1

            width = int(concat["slidewidth" + str(info.id)])
            height = int(concat["slideheight" + str(info.id)])
            x = int(concat["slidex" + str(info.id)])
            y = int(concat["slidey" + str(info.id)])
            x1 = x - width // 2
            y1 = y - height // 2
            x2 = x1 + width
            y2 = y1 + height
            info.vertexs = [[x1, y1], [x1, y2], [x2, y2], [x2, y1]]

        delt = concat.getlist('delete')
        if len(delt):
            for item in delt:
                pid = int(item)
                infos[pid].delt = 1
            ids = 0
            newinfos = []
            for item in infos:
                if item.delt != 1:
                    item.id = ids
                    ids = ids + 1
                    newinfos.append(item)
            infos = newinfos

        if (concat['newone'] == 'yes'):
            id = len(infos)
            midx = size[0] / 2
            midy = size[1] / 2
            ifonew = ifs.Info([[5 * midx / 6, 5 * midy / 6], [7 * midx / 6, 5 * midy / 6], [7 * midx / 6, 7 * midy / 6], [5 * midx / 6, 7 * midy / 6]], 1, '', '', id, False)
            ifonew.enable = 0
            infos.append(ifonew)

        request.session['infos'] = infos
        print("renewing..")
        yaki.renew(infos, settings.UPLOAD_ROOT + '/' + picname, settings.RESULT_ROOT + '/s_' + picname, settings.RESULT_ROOT + '/' + picname)

        return render(request, 'show.html', {'images': picname, 'infos': infos, 'oriname': oriname})
        # return render(request, 'show.html')
    # return HttpResponse(picname)
