from django.views import generic
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
import logging
from django.contrib.auth.models import User
from events.models import Event
from bugs.forms import NewTicketForm
from .models import Ticket
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.
@login_required()
def addTicket(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user
    if request.method == 'POST':
        new_ticket_form = NewTicketForm(data=request.POST)
        if new_ticket_form.is_valid():
            description = request.POST['description']
            title = request.POST['title']
            creator = user
            ticket_type = request.POST.get('ticket_type', False)
            event = event
            # TODO: to populate watchers and reviewers with default reviewers during some event
            # Need to create additional role "reviewers" and "watchers" for event
            # TODO: also need to develop attachments and to handle them in POST data
            # create_ticket(self, title, description, creator, is_bug, is_report, watchers, reviewers, event)
            new_ticket = Ticket.objects.create_ticket(title=title, description=description,
                                                      creator=creator, ticket_type=ticket_type, event=event)
            new_ticket.save()
            #return HttpResponseRedirect(reverse('events:event', kwargs={'pk':event_id}))
            return HttpResponseRedirect(reverse('bugs:eventTickets'))
        else:
            print(new_ticket_form.errors)
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        # TODO: need to handle default values for fields
        new_ticket_form = NewTicketForm()
    context = {"user": user, "event": event, "new_ticket_form": new_ticket_form}
    return render(request, 'bugs/new_ticket.html', context)


class TicketView(generic.DetailView):
    model = Ticket
    template_name = 'bugs/ticket.html'


class EventTickets(generic.ListView):
    model = Ticket
    template_name = 'bugs/ticket_list.html'
    context_object_name = 'all_tickets_list'

    # def get_queryset(self):
    #     """
    #    Return the last five published questions (not including those set to be
    #    published in the future).
    #    """
    #     return Ticket.objects.filter(event=Event)