from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import json
from .models import Text, Lanfiles


def files_view(request):
    if request.method == "POST":
        files = request.FILES.getlist('lanfile')
        for f in files:
            Lanfiles.objects.create(file=f)
            print(f"FILE: {f}")
        return redirect('lan')

def async_view(request):
    if request.method == "POST":

        ip = request.META.get('REMOTE_ADDR')
        data = json.loads(request.body)
        message = data['data']
        address = data['ip']
        text = data['text']

        Text.objects.create(texts=text)

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
        files = Lanfiles.objects.all()
        latest = Text.objects.latest('created_at')
        # print(f'The latest text: {latest.texts}')
        context = {
            'files':files,
            'latest': latest.texts,
        }
        return render(request, 'lan/locale.html', context)
    except Exception as e:
        # print(f"The error is: {e}")
        return render(request, 'lan/locale.html')