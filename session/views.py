from django.shortcuts import render, redirect
from django.http import  HttpResponse

# Create your views here.
def login(request):
    return render(request,'login.html')

def logout(request):
    return  redirect("/")

def login_process(request):
    # userAccount=request.GET["userAccount"]
    # userPassword= request.GET["userPassword"]
    userAccount = request.POST["userAccount"]
    userPassword = request.POST["userPassword"]
    print(userAccount,userPassword)
    return HttpResponse()

def check_session(request):
    pass
