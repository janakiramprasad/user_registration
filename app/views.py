from django.shortcuts import render

from app.forms import *

# Create your views here.

def registration(request):
    emud=UserForm()
    empd=ProfileForm()
    d={'emud':emud,'empd':empd}

    return render(request,'registration.html',d)
