from django.http import HttpResponse

from django.http import HttpRequest
def html(request):
    s = '''
    <html>
        <head>
        </head>
        <body>
            這是我的第一個網頁
        </body>
    </html>
    '''

    return HttpResponse(s)