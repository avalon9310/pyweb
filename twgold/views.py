from django.shortcuts import render, redirect


# Create your views here.

def html(request):
    request.session["currentPage"] = "/twgold"
    if 'userAccount' not in request.session:
        return redirect("/login")
    return render(request,'twgold.html')