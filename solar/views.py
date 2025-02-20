from django.shortcuts import render, redirect


def html(request):
    request.session["currentPage"] = "/solar"
    if 'userAccount' not in request.session:
        return redirect("/login")

    year_list = range(2000, 2025)
    return render(request, 'solar.html', {'year_list': year_list})


