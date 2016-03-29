from django.conf.urls import url

from . import views
from .views import EventDetailView

app_name = 'events'
urlpatterns = [
    # ex: /events/
    url(r'^$', views.events, name='events'),
    # ex: /events/5/add_participant/
    url(r'^(?P<event_id>[0-9]+)/add_participant/$', views.addParticipant, name='add_participant'),
    # ex: /events/5/delete_participant/
    url(r'^(?P<event_id>[0-9]+)/delete_participant/$', views.deleteParticipant, name='delete_participant'),
    # ex: /events/5/
    url(r'^(?P<pk>[0-9]+)/$', EventDetailView.as_view(), name='event'),
]

