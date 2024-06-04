from django.shortcuts import render, HttpResponse

def lan_view(request):
    return render(request, 'lan/locale.html')