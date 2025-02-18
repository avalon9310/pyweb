# Create your views here.
from django.shortcuts import render, redirect


def html(request):
    request.session["currentPage"] = "/travel"
    if 'userAccount' not in request.session:
        return redirect("/login")
    return render(request,'travel.html')