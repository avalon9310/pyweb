from django.shortcuts import render, redirect


# Create your views here.

def html(request):
    request.session["currentPage"] = "/twstock"
    if 'userAccount' not in request.session:
        return redirect("/login")
    return render(request,'twstock.html')