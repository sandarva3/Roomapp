from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Text, Lanfiles, FilesHistory
from pytz import timezone
import time
from datetime import datetime
import os
from django.conf import settings
from django.core.files.base import File as DjangoFile
import re

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
                'file':fileurl,
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
            FilesHistory.objects.create(file_name = f"Deleted: {file}", Faddress=IP)
            file.delete()

        return JsonResponse(1, safe=False)


def about_view(request):
    return render(request, 'lan/about.html')


def delFile_view(request, id):
    file = Lanfiles.objects.get(id=id)
    FilesHistory.objects.create(file_name=f"Deleted: {file}", Faddress=file.Faddress)
    file.delete()
    return redirect('lan')



@csrf_exempt
def largeFiles_view(request):
    if request.method == "POST":
        try:
            file_name = request.POST.get("filename")
            file_name = os.path.basename(file_name)
            file_name = re.sub(r'[<>:"/\\|?*]', '', file_name)  # Sanitize the file name
            print(f"RECEIVED LARGE FILE: {file_name}")

            chunk_index = int(request.POST.get("chunkIndex"))
            total_chunks = int(request.POST.get("totalChunks"))
            ipAddress = request.POST.get('ipAddress')
            chunk_file = request.FILES["chunkFile"]

            # Create a directory for storing the chunks
            upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads", file_name)
            print(f"Upload directory: {upload_dir}")
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            # Save each chunk in its respective file (chunk_0, chunk_1, etc.)
            chunk_file_path = os.path.join(upload_dir, f"chunk_{chunk_index}")
            print(f"Chunk file path: {chunk_file_path}")
            with open(chunk_file_path, 'wb+') as destination:
                for chunk_data in chunk_file.chunks():
                    destination.write(chunk_data)

            # Count the number of chunks that have been uploaded
            received_chunks = len([name for name in os.listdir(upload_dir) if name.startswith("chunk_")])
            print(f"Received chunks: {received_chunks}")

            # If all chunks are uploaded, assemble the file and save it to the database
            if received_chunks == total_chunks:
                ##We check if the lock file exists.
                lock_file_path = os.path.join(upload_dir, "assembly.lock")
                #if it doesn't exist then we create one. 
                if not os.path.exists(lock_file_path):
                    open(lock_file_path, 'w').close()
                    #After creating a lock file we begin to assemble the chunks.
                    Assemble(file_name, total_chunks, upload_dir, ipAddress)

                    #Why we created lock file? : So that two different processses don't conflict. If two users upload the same file simultaneously then
                    #it would cause conflict, their chunks would be uploaded in same directoy, and the one first device(process) which finish uploading chunk
                    #will create a lock file, after the lock file is created another process can't begin assembling(on line 98,99, and 101). 
                    #If we don't create lock file then two processes simultaneously being assembling and and the first one to finish assembling will start
                    #to delete chunks before another process finish assembling. So it creates conflict, to prevent that we created lock file.
                    #the lock file is just a checkmark, we could have used any .txt file with my name to check. assembly.lock more resonates and readable.

            return JsonResponse({'status': 'success', 'chunkIndex': chunk_index})

        except Exception as e:
            print(f"Error during File Upload: {e}")
            return HttpResponse("ERROR DURING FILE UPLOAD", status=500)
    else:
        return HttpResponse("INVALID REQUEST METHOD.", status=405)


def Assemble(file_name, total_chunks, upload_dir, ipAddress):
    current_time = int(time.time())
    final_dir = os.path.join(settings.MEDIA_ROOT, "lanmedia")
    final_path = os.path.join(final_dir, file_name)
    print(f"Final path: {final_path}")

    try:
        # Assemble the file from the chunks
        with open(final_path, 'wb') as final_file:
            for chunk_index in range(total_chunks):
                chunk_file_path = os.path.join(upload_dir, f"chunk_{chunk_index}")
                print(f"Assembling chunk file path: {chunk_file_path}")
                with open(chunk_file_path, 'rb') as chunk:
                    final_file.write(chunk.read())

        # Save the assembled file in the database
        try:
            with open(final_path, 'rb') as f:
                django_file = DjangoFile(f, name=file_name)  # Wrap the file with a name
                print(f"Saving file to database: {final_path}")
                Lanfiles.objects.create(file=django_file, Funix_time=current_time, Faddress=ipAddress)
                FilesHistory.objects.create(file_name= f"Uploaded: {django_file.file.name}", Faddress=ipAddress)
                print(f"File assembled and saved: {file_name} from IP: {ipAddress}")
        except Exception as e:
            print(f"FILE NOT SAVED TO DATABASE, DUE TO: {e}")

        # Delete the chunks after the full file is assembled
        print(f"THe total chunk is: {total_chunks}")
        for chunk_index in range(total_chunks):
            print(f"Deleting chunk : {chunk_index}")
            chunk_file_path = os.path.join(upload_dir, f"chunk_{chunk_index}")
            os.remove(chunk_file_path)

    finally:
        # Remove the lock file after assembly is completed
        lock_file_path = os.path.join(upload_dir, "assembly.lock")
        if os.path.exists(lock_file_path):
            os.remove(lock_file_path)

        
        # Optionally remove the upload directory if all chunks are deleted
        try:
            os.rmdir(upload_dir)
            os.remove(final_path)
            print("THE ASSEMBLED FILE IS DELETED(Not the one which is saved for database)")
        except Exception as e:
            print(f"Error deleting upload directory: {e}")




def files_view(request):
    if request.method == "POST":
        try:
            files = request.FILES.getlist('file')
            address = request.POST.get('ipAddress')
            current_time = int(time.time())
            for f in files:
                Lanfiles.objects.create(file=f, Funix_time=current_time, Faddress=address)
                FilesHistory.objects.create(file_name=f"Uploaded: {f.name}", Faddress=address)
                print(f" RECEIVED SMALL FILE: {f}")
                print(f"THE ADDRESS ALONG WITH FILE: {address}")
            context = {
                'status':1,
            }
            return JsonResponse(context)

        except Exception as e:
            print(f"An ERROR occured while user upload files: {e}")
            return HttpResponse("SOMETHING Went Wrong. Probably Due to slow network. Please Try again.")


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
        latest = ""
        filesurl = []
        try:
            latest = Text.objects.filter(Taddress=ipAd).latest('created_at').texts
        except:
            pass
        try:
            files = Lanfiles.objects.filter(Faddress=ipAd).all()
            print(f"The files are: {files}")
            for file in  files:
                file_url = request.build_absolute_uri(file.file.url)
                filesurl.append({'id':file.id, 'name': file, 'url':file_url})
                print(f"The ID of file {file} is: {file.id}")
        except Exception as e:
            print(f"Error in getting files: {e}")
        context = {
            'files': filesurl,
            'latest': latest,
            }
        return render(request, 'lan/locale.html', context)
    else:
        return redirect('first')