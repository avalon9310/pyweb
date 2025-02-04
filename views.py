from django.shortcuts import render
#模板 : MVC架構: Model/View/Controller
def second(request):
    return render(request,'second.html')

def third(request):
    return render(request, 'third.html')