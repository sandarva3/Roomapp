from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import json
from .models import Text, Lanfiles
from django.utils import timezone
import time

def lanAjax_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        fileid = data['code']
        file = Lanfiles.objects.get(id=fileid)
        fileurl = request.build_absolute_uri(file.file.url)
        print(f"Data Received: {data['data']}")
        print(f"FILEID: {fileid}")
        print(f"File URL: {fileurl}")

        context = {
            'response': 'Data received successfully',
            'filename':file.file.name,
            'file':fileurl
        }
        return JsonResponse(context)
    else:
        return JsonResponse({'error':'Data not received'}, status=400)


def delFile_view(request, id):
    file = Lanfiles.objects.get(id=id)
    file.delete()
    return redirect('lan')


def files_view(request):
    if request.method == "POST":
        files = request.FILES.getlist('lanfile')
        current_time = int(time.time())
        address = '27.34.64.148'
        for f in files:
            Lanfiles.objects.create(file=f, Funix_time=current_time, Faddress=address)
            print(f"FILE: {f}")
        return redirect('lan')


def async_view(request):
    if request.method == "POST":

        ip = request.META.get('REMOTE_ADDR')
        data = json.loads(request.body)
        message = data['data']
        address = data['ip']
        text = data['text']
        current_time = int(time.time())
        print(f"The ip is: {ip}")
        print(f"The address is: {address}")
        Text.objects.create(texts=text, Tunix_time=current_time, Taddress=address)

        # print(f"The message from client is: {message}")
        # print(f"The address of network is: {address}")
        # print(f"THE TEXT: {text}")
        # print(f"The IP address is: {ip}")

        latest_text = Text.objects.latest('created_at').texts

        context = {
            'reply': "I got your Public IP address",
            'device':ip,
            'network':address,
            'latest':latest_text
        }

        return JsonResponse(context)

    else:
        return JsonResponse(
            {'error': "I couldn't get your IP address"},
             status = 400
        )


def lan_view(request):
    try:
        client_ip = request.META.get('REMOTE_ADDR')
        print(f"THE CLIENT IP IS: {client_ip}")
        latest = Text.objects.latest('created_at')
        files = Lanfiles.objects.all()
        # print(f"WORKING: {files}")
        filesurl = []
        for file in  files:
            # print(f"The file name is: {file}")
            file_url = request.build_absolute_uri(file.file.url)
            # print(f"THe file url is: {file_url}")
            filesurl.append({'id':file.id, 'name': file, 'url':file_url})
        # print(f'The latest text: {latest.texts}')
        context = {
            'files': filesurl,
            'latest': latest.texts,
        }
        return render(request, 'lan/locale.html', context)
    except Exception as e:
        # print(f"The error is: {e}")
        return render(request, 'lan/locale.html')