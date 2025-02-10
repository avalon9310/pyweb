from django.shortcuts import render
#模板 : MVC架構: Model/View/Controller
def html_01(request):
    return render(request, 'static/01.html')

def html_02(request):
    return render(request, 'static/02.html')

def html_03(request):
    return render(request, 'static/03.html')