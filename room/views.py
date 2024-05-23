from django.shortcuts import render, HttpResponse, redirect
from .models import Room, Files
from django.utils import timezone
from .forms import TimeForm
import time
import threading


def home_view(request):
    if request.method == "POST":
        form = TimeForm(request.POST)
        
        if form.is_valid():
            text = request.POST.get('text')
            files = request.FILES.getlist('files')
            time_choice = form.cleaned_data['time_choice']
            if time_choice == "1 hour":
                validation = 30
            elif time_choice == "4 hour":
                validation = 14400
            elif time_choice == "12 hour":
                validation = 43200
            elif time_choice == "1 day":
                validation = 86400
            
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
            }
            return render(request, 'room/home.html', context)

        else:
            return HttpResponse("Something went wrong in your form submission. Enter valid information. Try again.")

    else:
        unix_time = time.time()
        seconds = int(unix_time)
        form = TimeForm()
        current_time = timezone.now()
        print(f"TIME : {current_time}")
        print(f"UNIX TIME IS: {seconds}")
        return render(request,'room/home.html',{'form':form})


def room_view(request):
    if request.method == "POST":
        code = request.POST.get('code')
        print(f"Is this working? code : {code}")
        strCode = str(code)
        if strCode[:4] == "http":
            link = strCode[27:]
            print(f"the code from link is: {link}")
            room = Room.objects.get(code=link)
            files = room.files.all()
        else:
            print(f"The code is: {code}")
            room = Room.objects.get(code=code)
            files = room.files.all()
        
        context = {
            'room':room,
            'files':files,
        }
        return render(request, 'room/room.html', context)


def link_view(request, uuid):
    print(f"THE UUID: {uuid}")
    try: 
        room = Room.objects.get(code=uuid)
        files = room.files.all()
        context = {
            'room':room,
            'files':files,
        }
        return render(request, 'room/room.html', context)
    except (Room.objects.get(code=uuid)).DoesNotExist:
        return HttpResponse("The room is not found! Please Enter valid link.", status=404)