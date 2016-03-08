from django.conf.urls import url

from . import views

app_name = 'events'
urlpatterns = [
    # ex: /events/
    url(r'^$', views.events, name='events'),
    # ex: /events/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='event'),
]

