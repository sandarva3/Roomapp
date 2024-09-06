from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Text, Lanfiles
from pytz import timezone
import time
from datetime import datetime
import os
from django.conf import settings
from django.core.files import File

def lanAjax_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            fileid = data['code']
            file = Lanfiles.objects.get(id=fileid)
            fileurl = request.build_absolute_uri(file.file.url)
            print(f"FILEID: {fileid}")
            print(f"File URL: {fileurl}")

            context = {
                'response': 'Data received successfully',
                'filename':file.file.name[9:],
                'file':fileurl
            }
            return JsonResponse(context)
        except Exception as e:
            print(f"ERROR OCCURED TO DOWNLOAD FILE: {e}")
    else:
        return JsonResponse({'error':'Data not received'}, status=400)


def faq_view(request):
    return render(request, 'lan/faq.html')


def removeAllFiles_view(request):
    if (request.method == "POST"):
        data = json.loads(request.body)
        IP = data['ip']
        files = Lanfiles.objects.filter(Faddress=IP)
        for file in files:
            file.delete()

        return JsonResponse(1, safe=False)


def about_view(request):
    return render(request, 'lan/about.html')


def delFile_view(request, id):
    file = Lanfiles.objects.get(id=id)
    file.delete()
    return redirect('lan')

@csrf_exempt
def files_view(request):
    if request.method == "POST":
        try:
            file_name = request.POST.get('filename')
            chunk_index = int(request.POST.get('chunkIndex'))
            total_chunks = int(request.POST.get('totalChunks'))
            ipAddress = request.POST.get('ipAddress')
            chunk_file = request.FILES['chunk_file']
        
            # Create a directory for storing the chunks
            upload_dir = os.path.join('media/uploads', file_name)
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            # Save each chunk in its respective file (chunk_0, chunk_1, etc.)
            chunk_file_path = os.path.join(upload_dir, f'chunk_{chunk_index}')
            with open(chunk_file_path, 'wb+') as destination:
                for chunk_data in chunk_file.chunks():
                    destination.write(chunk_data)

            # Count the number of chunks that have been uploaded
            received_chunks = len([name for name in os.listdir(upload_dir) if name.startswith('chunk_')])
            #it appends name in array and len() calculates total number of names(or chunks here).
            #IT does the same thing:
            ''' 
            all_items = os.listdir(upload_dir)
            filtered_items = []
            for name in all_items:
                if name.startswith('chunk_'):
                    filtered_items.append(name)
            received_chunks = len(filtered_items)
            '''

            # If all chunks are uploaded, assemble the file and save it to the database
            if received_chunks == total_chunks:
                Assemble(file_name, total_chunks, upload_dir, ipAddress)
            
            return JsonResponse({'status': 'success', 'chunkIndex': chunk_index})
        
        except Exception as e:
            print(f"Error during File Upload: {e}")
            return HttpResponse("ERROR DURING FILE UPLOAD", status = 500)
    else:
        return HttpResponse("INVALID REQUEST METHOD.", status = 405)


def Assemble(file_name, total_chunks, upload_dir, ipAddress):
    # Path to store the final assembled file
    current_time = int(time.time())
    final_path = os.path.join('media/lanmedia', file_name)
    with open(final_path, 'wb') as final_file:
        for chunk_index in range(total_chunks):
            chunk_file_path = os.path.join(upload_dir, f'chunk_{chunk_index}')
            with open(chunk_file_path, 'rb') as chunk:
                final_file.write(chunk.read())
    #save the assembled file in db
    with open(final_path, 'rb') as f:
        file = File(f)
        Lanfiles.objects.create(file=file, Funix_time=current_time, Faddress=ipAddress)

    for chunk_index in range(total_chunks):
        chunk_file_path = os.path.join(upload_dir, f'chunk_{chunk_index}')
        os.remove(chunk_file_path)


'''
def files_view(request):
    if request.method == "POST":
        try:
            files = request.FILES.getlist('file')
            address = request.POST.get('ipAddress')
            current_time = int(time.time())
            for f in files:
                Lanfiles.objects.create(file=f, Funix_time=current_time, Faddress=address)
                print(f"FILE: {f}")
                print(f"THE ADDRESS ALONG WITH FILE: {address}")
            context = {
                'status':1,
            }
            return JsonResponse(context)

        except Exception as e:
            print(f"An ERROR occured while user upload files: {e}")
            return HttpResponse("SOMETHING Went Wrong. Probably Due to slow network. Please Try again.")
'''

def async_view(request):
    if request.method == "POST":

        data = json.loads(request.body)
        address = data['ip']
        text = data['text']
        current_time = int(time.time())
        print(f"The address is: {address}")
        Text.objects.create(texts=text, Tunix_time=current_time, Taddress=address)

        # print(f"The message from client is: {message}")
        # print(f"The address of network is: {address}")
        # print(f"THE TEXT: {text}")
        # print(f"The IP address is: {ip}")

        latest_text = Text.objects.latest('created_at').texts

        context = {
            'reply': "I got your Public IP address",
            'network':address,
            'latest':latest_text
        }

        return JsonResponse(context)

    else:
        return JsonResponse(
            {'error': "I couldn't get your IP address"},
             status = 400
        )


def first_view(request):
    return render(request, 'lan/getip.html')


def lan_view(request):
    ipAd = None
    try:
        data = json.loads(request.body)
        ipAd = data['ipAd']
        print(f"IP ADDRESS THIS TIME: {ipAd}")
    except:
        pass
    if ipAd != None:
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
            #print(f"IP ADDRESS second TIME: {ipAd}")
            return render(request, 'lan/locale.html', context)
        except Exception as e:
            print(f"Error in getting details: {e}")
            return render(request, 'lan/locale.html')
    else:
        return redirect('first')