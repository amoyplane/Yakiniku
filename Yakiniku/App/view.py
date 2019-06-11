from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
import os
import random
from PIL import Image
from django.conf import settings
from . import yakimain as yaki
from . import infostruct as ifs


def runmain(name):
    print('Processing ' + name + ' ... ')
    print(settings.UPLOAD_ROOT)
    print(settings.RESULT_ROOT)
    ret = yaki.doall(settings.UPLOAD_ROOT + '/' + name, settings.RESULT_ROOT + '/s_' + name, settings.RESULT_ROOT + '/' + name)
    return ret


def upload(request):
    if request.method == 'GET':
        t = random.randint(1, 4)
        return render(request, 'upload.html', {'images': t})
    elif request.method == 'POST':
        obj = request.FILES.get('pic')
        if obj == None:
            return render(request, 'upload.html')
        f = open(os.path.join('upload', obj.name), 'wb')
        for line in obj.chunks():
            f.write(line)
        f.close()

        img = Image.open(os.path.join('upload', obj.name))

        ret = runmain(obj.name)

        request.session['infos'] = ret
        request.session['picname'] = obj.name
        request.session['size'] = [img.size[0], img.size[1]]

        return HttpResponseRedirect('show.html')
        # return show(request, obj.name)
        # return HttpResponse(obj.name)


def show(request):
    picname = request.session.get('picname')
    infos = request.session.get('infos')
    size = request.session.get('size')
    print(picname)
    if request.method == 'GET':
        return render(request, 'show.html', {'images': picname, 'infos': infos})
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
            infos[pid].enable = 1
        for info in infos:
            key = "trans" + str(info.id)
            info.trans = concat[key]
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
        for item in delt:
            pid = int(item)
            for info in infos:
                if info.id > pid:
                    info.id = info.id - 1
            del infos[pid]
        if (concat['newone'] == 'yes'):
            id = len(infos)
            midx = size[0] / 2
            midy = size[1] / 2
            ifonew = ifs.Info([[5 * midx / 6, 5 * midy / 6], [7 * midx / 6, 5 * midy / 6], [7 * midx / 6, 7 * midy / 6], [5 * midx / 6, 7 * midy / 6]], 1, '', '', id, False)
            infos.append(ifonew)

        request.session['infos'] = infos
        print("renewing..")
        yaki.renew(infos, settings.UPLOAD_ROOT + '/' + picname, settings.RESULT_ROOT + '/s_' + picname, settings.RESULT_ROOT + '/' + picname)

        return render(request, 'show.html', {'images': picname, 'infos': infos})
        # return render(request, 'show.html')
    # return HttpResponse(picname)
