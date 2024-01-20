from django.shortcuts import render

from app.forms import *

from django.http import HttpResponse

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

            return HttpResponse('data inserted sucessfully')
        else:
            return HttpResponse('invalida data')


    return render(request,'registration.html',d)
