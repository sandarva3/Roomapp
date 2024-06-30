from django.shortcuts import render, HttpResponse, redirect
from .models import Room, Files
from .forms import TimeForm
import time
from pytz import timezone
import pytz
from datetime import datetime
from django.http import JsonResponse
import json


def getNepTime(utcTime):
    nepTime = timezone('Asia/Kathmandu')        
    return ((utcTime).astimezone(nepTime))


def ajax_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        fileid = data['code']
        file = Files.objects.get(id=fileid)
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


def home_view(request):
    if request.method == "POST":
        form = TimeForm(request.POST)
        
        if form.is_valid():
            try:
                text = request.POST.get('text')
                files = request.FILES.getlist('files')
                time_choice = form.cleaned_data['time_choice']
                if time_choice == "1 hour":
                    validation = 3600
                elif time_choice == "4 hour":
                    validation = 14400
                elif time_choice == "12 hour":
                    validation = 43200
                elif time_choice == "1 day":
                    validation = 86400
                elif time_choice == "3 days":
                    validation = 259200

                unix_time = time.time()
                seconds = int(unix_time)
                ttime = validation + seconds
                print(f"text: {text}, files: {files}")
                print(f"The time choice is: {time_choice}")
                print(f"The validation is: {validation} seconds.")
                room = Room.objects.create(text=text, total_time=ttime)

                for f in files:
                    Files.objects.create(room=room, file=f)
                    print(f"File {f}")

                room.save()
                print(f"The ROOM CODE IS : {room.code}")
                context = {
                'room_code': room.code,
                'room_url': request.build_absolute_uri(f'room/{room.code}'),
                'state': True,
                }
                return render(request, 'room/home.html', context)
            
            except:
                return HttpResponse("Something Unexpected Went Wrong. Please Try again.")

        else:
            return HttpResponse("Something went wrong in your form submission. Enter valid information. Try again.")

    else:
        form = TimeForm()
        return render(request,'room/home.html',{'form':form})


def room_view(request):
    Rampm = None
    Tampm = None
    if request.method == "POST":
        try:
            code = request.POST.get('code')
            print(f"Is this working? code : {code}")
            strCode = str(code)
            if strCode[:4] == "http":
                link = strCode[27:]
                print(f"the code from link is: {link}")
                room = Room.objects.get(code=link)
                files = room.files.all()
                till_date = datetime.fromtimestamp(room.total_time, tz=pytz.utc)

            else:
                print(f"The code is: {code}")
                room = Room.objects.get(code=code)
                files = room.files.all()
                print(f"ROOM FOUND: {room}")
                print(f"FILES IN ROOM: {files}")
                till_date = datetime.fromtimestamp(room.total_time, tz=pytz.utc)

            NeproomTime = getNepTime(room.created_at)
            NeptillTime = getNepTime(till_date)
            print(f"Room creation time: {NeproomTime}")
            print(f"TILL TIME: {NeptillTime}")
            if (NeproomTime.hour < 12):
                Rampm = "AM"
            else:
                Rampm = "PM"
            if (NeptillTime.hour < 12):
                Tampm = "AM"
            else:
                Tampm = "PM"

            context = {
                'room':room,
                'files':files,
                'roomTime':str(NeproomTime)[:19],
                'tillTime':str(NeptillTime)[:19],
                'Rampm':Rampm,
                'Tampm':Tampm,
                # 'till_date': timezone.localtime(till_date),
            }
            
            return render(request, 'room/room.html', context)
        except Exception as e:
            print(f"THE ERROR IS : {e}")
            return HttpResponse("The room you're trying to access could've been already vanished. OR Please make sure your code/link is Valid.", status=404)
    else:
        return HttpResponse("SOMETHING WENT WRONG. TRY AGAIN.")
        

def link_view(request, uuid):
    Rampm = None
    Tampm = None
    print(f"THE UUID: {uuid}")
    try: 
        room = Room.objects.get(code=uuid)
        files = room.files.all()
        till_date = datetime.fromtimestamp(room.total_time, tz=pytz.utc)

        NeproomTime = getNepTime(room.created_at)
        NeptillTime = getNepTime(till_date)
        print(f"Room creation time: {NeproomTime}")
        print(f"TILL TIME: {NeptillTime}")
        if (NeproomTime.hour < 12):
            Rampm = "AM"
        else:
            Rampm = "PM"
        if (NeptillTime.hour < 12):
            Tampm = "AM"
        else:
            Tampm = "PM"
        context = {
            'room':room,
            'files':files,
            'roomTime':str(NeproomTime)[:19],
            'tillTime':str(NeptillTime)[:19],
            'Rampm':Rampm,
            'Tampm':Tampm,
        }
        return render(request, 'room/room.html', context)

    except:
        return HttpResponse("The room you're trying to access could've been already vanished. OR Please make sure your code/link is Valid.", status=404)