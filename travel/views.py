# Create your views here.
from django.shortcuts import render

def html(request):
    return render(request,'travel.html')