from django.shortcuts import render

from app.forms import *

from django.http import HttpResponse,HttpResponseRedirect

from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate,login,logout
from django.urls import reverse




# Create your views here.

def registration(request):
    emud=UserForm()
    empd=ProfileForm()
    d={'emud':emud,'empd':empd}
    
    if request.method=='POST' and request.FILES:
        usdo=UserForm(request.POST)
        psdo=ProfileForm(request.POST,request.FILES)

        if usdo.is_valid() and psdo.is_valid():
            mufdo=usdo.save(commit=False)
            pw=usdo.cleaned_data['password']
            mufdo.set_password(pw)
            mufdo.save()

            mpdo=psdo.save(commit=False)
            mpdo.username=mufdo
            mpdo.save()

            send_mail('registration',
                      'thanku for registration ',
                      'janakiramtj7@gmail.com',
                      [mufdo.email],
                      fail_silently=False,
                      )



            return HttpResponse('data inserted sucessfully')
        else:
            return HttpResponse('invalida data')


    return render(request,'registration.html',d)

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    


    return render(request,'home.html')



def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)

        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('invalid data')

    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



@login_required
def display_details(request):
    un=request.session.get('username')
    uo=User.objects.get(username=un)
    po=Profile.objects.get(username=uo)
    d={'uo':uo,'po':po}    

    return render(request,'display_details.html',d)


@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        Uo=User.objects.get(username=username)
        Uo.set_password(pw)
        Uo.save()

        return HttpResponse('password changed sucessfullly')

    return render(request,'change_password.html')

def reset_password(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        LUO=User.objects.filter(username=username)
        if LUO:
            UO=LUO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponse('password is changed successfully')
        else:
            return HttpResponse('your name is not matching with my data base')
    return render(request,'reset_password.html')