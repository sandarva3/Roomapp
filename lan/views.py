from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import json
from .models import Text, Lanfiles
from django.utils import timezone
import time
import requests

def lanAjax_view(request):
    if request.method == "POST":
        try:
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
        except Exception as e:
            print(f"ERROR OCCURED TO DOWNLOAD FILE: {e}")
    else:
        return JsonResponse({'error':'Data not received'}, status=400)


def delFile_view(request, id):
    file = Lanfiles.objects.get(id=id)
    file.delete()
    return redirect('lan')


def files_view(request):
    if request.method == "POST":
        try:
            response = requests.get('https://api.ipify.org?format=json')
            data = response.json()
            ipAd = data.get("ip")
            try:
                Dip = request.META.get('REMOTE_ADDR')
                files = request.FILES.getlist('lanfile')
                #address = request.POST.get('addr')
                current_time = int(time.time())
                for f in files:
                    Lanfiles.objects.create(file=f, Funix_time=current_time, Faddress=ipAd)
                    print(f"FILE: {f}")
                    print(f"THE ADDRESS ALSO ARRIVED ALONG WITH FILE: {ipAd}")
                return redirect('lan')
            except Exception as e:
                print(f"An ERROR occured while user upload files: {e}")
                return HttpResponse("SOMETHING Went Wrong. Probably Due to slow network. Please Try again.")
        except Exception as e:
            print(f"IPIFY ERROR: {e}")


def async_view(request):
    if request.method == "POST":

        Dip = request.META.get('REMOTE_ADDR')
        data = json.loads(request.body)
        message = data['data']
        address = data['ip']
        text = data['text']
        current_time = int(time.time())
        print(f"The ip is: {Dip}")
        print(f"The address is: {address}")
        Text.objects.create(texts=text, Tunix_time=current_time, Taddress=address)

        # print(f"The message from client is: {message}")
        # print(f"The address of network is: {address}")
        # print(f"THE TEXT: {text}")
        # print(f"The IP address is: {ip}")

        latest_text = Text.objects.latest('created_at').texts

        context = {
            'reply': "I got your Public IP address",
            'device':Dip,
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
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        ipAd = data.get("ip")
        print(f"THE PUBLIC IP ADDRESS FROM IPIFY IS: {ipAd}")
        try:
            latest = Text.objects.filter(Taddress=ipAd).latest('created_at')
            files = Lanfiles.objects.filter(Faddress=ipAd).all()
            filesurl = []
            for file in  files:
                file_url = request.build_absolute_uri(file.file.url)
                filesurl.append({'id':file.id, 'name': file, 'url':file_url})
            context = {
                'files': filesurl,
                'latest': latest.texts,
            }
            return render(request, 'lan/locale.html', context)
        except Exception as e:
            print(f"Error in getting details: {e}")
            return render(request, 'lan/locale.html')
    
    except Exception as e:
        print(f"IPIFY ERROR: {e}")