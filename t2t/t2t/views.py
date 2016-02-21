from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render

from polls.models import Event

def main(request):
    return render(request, 'polls/jumbotron.html', {})	
def contacts(request):
    return render(request, 'polls/contacts.html', {})
def events(request):
	next_events_list = Event.objects.order_by('-start_time')
	context = {"next_events_list":next_events_list}
	return render(request, 'polls/events.html', context)
def event(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	return render(request, 'polls/event.html', {'event': event})