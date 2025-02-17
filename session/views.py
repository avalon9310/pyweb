from django.shortcuts import render, redirect
from django.http import  HttpResponse
import mysql.connector as mysql
from G import G
# Create your views here.
def login(request):
    return render(request,'login.html')

def logout(request):
    return redirect("/")

def login_process(request):
    # userAccount=request.GET["userAccount"]
    # userPassword= request.GET["userPassword"]
    userAccount = request.POST["userAccount"]
    userPassword = request.POST["userPassword"]
    print(userAccount,userPassword)

    conn=mysql.connect(
        host=G.dbHost,
        user=G.dbAccount,
        password=G.dbPassword,
        database=G.db
    )
    cursor=conn.cursor()
    cmd="select * from 會員資料"
    cursor.execute(cmd)
    rs=cursor.fetchall()
    for r in rs:
        print(r)

    return HttpResponse("Login processed successfully.")

def check_session(request):
    pass


