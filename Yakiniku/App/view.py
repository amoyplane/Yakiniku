from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
import os


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

        request.session['picname'] = obj.name

        return HttpResponseRedirect('show.html')
        # return show(request, obj.name)
        # return HttpResponse(obj.name)


def show(request):
    picname = request.session.get('picname')
    print(picname)
    if request.method == 'GET':
        return render(request, 'show.html', {'images': picname})
        # return render(request, 'show.html')
    # return HttpResponse(picname)
