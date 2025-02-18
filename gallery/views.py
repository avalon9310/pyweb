from django.shortcuts import render, redirect


def html(request):
    request.session["currentPage"] = "/gallery"
    if 'userAccount' not in request.session:
        return redirect("/login")
    return render(request,'gallery.html')
