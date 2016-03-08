from django.shortcuts import render

from django.views import generic
from .models import Event


# Create your views here.
def events(request):
    next_events_list = Event.objects.order_by('-start_time')
    context = {"next_events_list": next_events_list}
    return render(request, 'events/events.html', context)


class DetailView(generic.DetailView):
    model = Event
    template_name = 'events/event.html'
