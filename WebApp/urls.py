"""WebApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from App import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin


urlpatterns = [ 
    url(r'^$', views.home),
    url(r'^get/$', views.get),
    url(r'^update_log_in_db/$', views.update_log_in_db),
    url(r'^get_log_entry/$', views.get_log_entry),
    url(r'^admin/', admin.site.urls)
] + staticfiles_urlpatterns()
