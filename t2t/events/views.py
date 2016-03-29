from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import logging

from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from .models import Event
from django.contrib.auth.models import User

# Create your views here.
def events(request):
    next_events_list = Event.objects.order_by('-start_time')
    context = {"next_events_list": next_events_list}
    return render(request, 'events/events.html', context)


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event.html'

@login_required
def addParticipant(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user

    # trying to understand if the user is already registered as a participant:
    if user not in event.users.all():
        # check that current number of registered users is not bigger than max:
        if event.current_participants_number < event.max_participants_number:
            event.current_participants_number +=1
            event.users.add(user)
            event.save()
        else:
            # action: add handler if user tries to register, but the number of registered users is already
            # reached max
            logging.error('Number of registered users is already reached max')
            pass
    else:
        # action: insert a handler in case user is already added as a participant
        logging.error('User is already added as a participant')
        pass
    return HttpResponseRedirect(reverse('main'))

@login_required
def deleteParticipant(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user

    # trying to understand if the user is already registered as a participant:
    if user in event.users.all():
        event.current_participants_number -=1
        event.users.remove(user)
        event.save()
    else:
        # action: add handler if user tries to register, but the number of registered users is already
        # reached max
        logging.error('User is not in the participants list for this event')

    return HttpResponseRedirect(reverse('main'))