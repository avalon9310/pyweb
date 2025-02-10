"""
URL configuration for pyweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import first,views
import home.views as home #from home import views as home
import gallery.views as gallery
import travel.views as travel
import tools.views as tools
import twstock.views as twstock
import twgold.views as twgold
import session.views as session
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('first/', first.html),
    path('', home.html),
    path('gallery/', gallery.html),
    path('travel/', travel.html),
    path('tools/', tools.html),
    path('twstock/', twstock.html),
    path('twgold/', twgold.html),
    path('01/', views.html_01),
    path('02/', views.html_02),
    path('03/', views.html_03),
    path('login/', session.login),
    path('logout/', session.logout),
    path('login_process/', session.login_process),
    path('check_session/', session.check_session),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
