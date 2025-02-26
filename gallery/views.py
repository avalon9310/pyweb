from django.shortcuts import render, redirect
from G import G

def html(request):
    info = G.saveHistory(request, 'gallery')
    request.session["currentPage"] = "/gallery"
    if 'userAccount' not in request.session:
        return redirect("/login")
    return render(request,'gallery.html',{"info":info[1]})
