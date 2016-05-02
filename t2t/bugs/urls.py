from django.conf.urls import url

from . import views
from .views import EventTickets, TicketView
from events.models import Event

app_name = 'bugs'
urlpatterns = [
    # ex: /bugs/
    url(r'^$', EventTickets.as_view(), name='eventTickets'),
    # ex: /bugs/5/
    url(r'^(?P<pk>[0-9]+)/$', views.TicketView.as_view(), name='viewTicket'),
    # ex: /bugs/add
    url(r'^add/(?P<event_id>[0-9]+)/$', views.addTicket, name='addTicket'),
    # ex: /bugs/event/
]