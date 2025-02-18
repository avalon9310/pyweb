import time

from django.shortcuts import render, redirect
from django.http import  HttpResponse
import mysql.connector as mysql
from G import G
chance=3
# Create your views here.
def login(request):
    return render(request,'login.html')

def logout(request):
    if 'userAccount' in request.session:
        del request.session["userAccount"]
    return redirect("/")

def login_process(request):
    # userAccount=request.GET["userAccount"]
    # userPassword= request.GET["userPassword"]
    userAccount = request.POST["userAccount"].replace("'","\\'")
    userPassword = request.POST["userPassword"].replace("'","\\'")
    print(userAccount,userPassword)

    conn=mysql.connect(
        host=G.dbHost,
        user=G.dbAccount,
        password=G.dbPassword,
        database=G.db
    )
    cursor=conn.cursor()
    cmd=f"select * from 會員資料 where userAccount='{userAccount}' and userPassword='{userPassword}'"
    cursor.execute(cmd)
    rs=cursor.fetchall()
    conn.close()
    if len(rs)>0:
        request.session['userAccount']=userAccount
        if 'currentPage' in request.session:
            return redirect(request.session["currentPage"])
        else:
            return redirect("/")
    else:
        if "loginCount" not in request.session:
            request.session["loginCount"] = 1
        else:
            request.session["loginCount"] +=1;
        time.sleep(3)

        if request.session['loginCount'] >=chance:
            return redirect("/reject")
        return render(request, 'login.html',{"login":"error"})


def check_session(request):
    pass

def reject(request):
    return  render(request, 'reject.html')


