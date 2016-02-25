"""t2t URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from . import views

urlpatterns = [
    ##wnat to include main page here:
	url('^register/', CreateView.as_view(
            template_name='register.html',
            form_class=UserCreationForm,
            success_url='/'
	), name="register"),
    url('^accounts/', include('django.contrib.auth.urls')),
	url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
	##ex: http://127.0.0.1:8000
	url(r'^$', views.main, name='main'),
	url(r'^contacts/', views.contacts, name='contacts'),
	##needed for usage of authorization forms:
	url('^', include('django.contrib.auth.urls')),
	## ex: /events/5/
    url(r'^events/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='event'),
	## ex: /events/
	url(r'^events/',  views.events, name='events'),
]
