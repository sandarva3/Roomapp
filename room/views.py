from django.shortcuts import render, HttpResponse, redirect
from .models import Room
from .forms import RoomForm


def home_view(request):
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        text = request.POST.get('text')
        if form.is_valid():
            files = form.cleaned_data['file']
            room = Room.objects.create(text=text, file=files)
            room.save()
            print(f"The ROOM CODE IS : {room.code}")
            context = {
            'room_code': room.code,
            'room_url': request.build_absolute_uri(f'room/{room.code}'),
            }
        return render(request, 'room/home.html', context)
    else:
        form = RoomForm()
        return render(request,'room/home.html', {'form':form})


def room_view(request):
    if request.method == "POST":
        code = request.POST.get('code')
        print(f"Is this working? code : {code}")
        strCode = str(code)
        if strCode[:4] == "http":
            link = strCode[27:]
            print(f"the code from link is: {link}")
            room = Room.objects.get(code=link)
        else:
            print(f"The code is: {code}")
            room = Room.objects.get(code=code)
        return render(request, 'room/room.html', {'room': room})


def link_view(request, uuid):
    try: 
        room = Room.objects.get(code=uuid)
        return render(request, 'room/room.html', {'room':room.text})
    except (Room.objects.get(code=uuid)).DoesNotExist:
        return HttpResponse("The room is not found! Please Enter valid link.", status=404)