from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
import os

from django.conf import settings
from . import yakimain as yaki


def runmain(name):
    print('Processing ' + name + ' ... ')
    print(settings.UPLOAD_ROOT)
    print(settings.RESULT_ROOT)
    ret = yaki.doall(settings.UPLOAD_ROOT + '/' + name, settings.RESULT_ROOT + '/s_' + name, settings.RESULT_ROOT + '/' + name)
    return ret


def upload(request):
    if request.method == 'GET':
        return render(request, 'upload.html')
    elif request.method == 'POST':
        obj = request.FILES.get('pic')
        if obj == None:
            return render(request, 'upload.html')
        f = open(os.path.join('upload', obj.name), 'wb')
        for line in obj.chunks():
            f.write(line)
        f.close()

        ret = runmain(obj.name)

        request.session['infos'] = ret
        request.session['picname'] = obj.name

        return HttpResponseRedirect('show.html')
        # return show(request, obj.name)
        # return HttpResponse(obj.name)


def show(request):
    picname = request.session.get('picname')
    infos = request.session.get('infos')
    print(picname)
    if request.method == 'GET':
        return render(request, 'show.html', {'images': picname, 'infos': infos})
    elif request.method == 'POST':
        concat = request.POST
        print(concat)
        return render(request, 'show.html', {'images': picname, 'infos': infos})
        # return render(request, 'show.html')
    # return HttpResponse(picname)
