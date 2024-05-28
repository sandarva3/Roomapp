from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.forms import EmailField, PasswordInput, TextInput
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth


class CustomUserCreationForm(CustomUserCreationForm):
    email = EmailField(label='email',required=True, widget=TextInput(attrs={'placeholder': 'Email', 'class': 'email-input'}))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

def register_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home', username=user.username)
    else:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect('home', username=user.username)
            else:
                return render(request, 'Trace/register.html', {'form': form})
        else:
            form = CustomUserCreationForm()
        return render(request, 'Trace/register.html', {'form': form})


def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home', username=user.username)
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home', username=user.username)
        else:
            form = AuthenticationForm()
        context = {'form': form}
        if request.user.is_authenticated:
            context['user'] = request.user
        return render(request, 'Trace/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def home_screen_view(request, username):
    try:
        user = CustomUser.objects.get(username=username)
        items = Item.objects.filter(user=request.user).order_by("-date")
        context = {'items': items}
        return render(request, 'Trace/home.html', context)
    except ObjectDoesNotExist:
        return render(request, "Trace/not.html")

def guestHome_view(request):
    return render(request, "Trace/guestHome.html")


def whole_view(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse("You must be registered to view this page")
    try:
        items = Whole.objects.filter(user=user).annotate(month=TruncMonth('date')).order_by('-month')
        monthly_totals = items.values('month').annotate(total=Sum('number')).order_by('-month')

        monthly_data = {}
        for month in monthly_totals:

            monthly_items = items.filter(month=month['month']).order_by('date')
            monthly_data[month['month']] = {
                'items': list(monthly_items),
                'total': month['total']
            }

        context = {
            'monthly_data': monthly_data,
            'monthly_totals':monthly_totals,
        }
        return render(request, "Trace/whole.html", context)
    except CustomUser.DoesNotExist:
        return render(request, "Trace/not.html")


def wholeadd_view(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            text = request.POST.get('text')
            number = request.POST.get('number')
            date = request.POST.get('date')
            today = request.POST.get('today')
            if date:
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            elif today:
                date = datetime.date.today()
            else:
                date = None
            item = Whole(user=user,text=text, number=number, date=date)
            item.save()
            return redirect('wholething')
        else:
            return render(request, "Trace/wholeadd.html")
    else:
        return HttpResponse("You must be registered to view this page !")
    return redirect('login')


def guestAdd_view(request):
    return render(request, "Trace/guestAdd.html")


def add_view(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            text = request.POST.get('text')
            number = request.POST.get('number')
            is_purchased = request.POST.get('timeoptions') == 'purchased'
            notpurchased = request.POST.get('timeoptions') == 'notpurchased'
            date = request.POST.get('date')
            today = request.POST.get('today')
            if date:
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            elif today:
                date = datetime.date.today()
            else:
                date = None
            item = Item(user=user,text=text, number=number, is_purchased=is_purchased, notpurchased=notpurchased, date=date)
            item.save()
            return redirect('home', username=user.username)
        else:
            context = {}
            return render(request, 'Trace/add.html',context)
    else:
        return HttpResponse("You must be registered to view this page !")
    return redirect('login')

@login_required(login_url='/login/')
def remove_view(request, id):
    user=request.user
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('home', username=user.username)

@login_required(login_url='/login/')
def Wremove_view(request, id):
    user=request.user
    item = Whole.objects.get(id=id)
    item.delete()
    return redirect('wholething')
