from django.http import HttpResponseRedirect
from django.views import generic
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
import logging
from django.contrib.auth.decorators import login_required
from .forms import NewMessageForm
from .models import Message, MessageThread
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your views here.
@login_required()
def view_messages_page(request):
    return render(request, 'mess/messages_main.html', {})


@login_required()
def new_message_page(request):
    user = request.user
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        new_message_form = NewMessageForm(data=request.POST)
        if new_message_form.is_valid():
            to_user_id = request.POST['to_user']
            text = request.POST['text']
            to_user = User.objects.get(id=to_user_id)
            message = Message.objects.create_message(from_user=user, to_user=to_user, text=text)
            context = {"new_message_form": new_message_form, "message_status": 1}
            return render(request, 'mess/new_message.html', context)
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        new_message_form = NewMessageForm()
        context = {"new_message_form": new_message_form}
        return render(request, 'mess/new_message.html', context)


class UserMessages(generic.ListView):
    model = Message
    template_name = 'mess/user_messages.html'
    context_object_name = 'all_user_messages'
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(to_user=user)|Q(from_user=user))


class UserThreads(generic.ListView):
    model = MessageThread
    template_name = 'mess/user_threads.html'
    context_object_name = 'all_user_threads'

    def get_queryset(self):
        user = self.request.user
        return MessageThread.objects.filter(users=user)

    #TODO: need to send to templates: user names for all threads,
    #                                 along with last messages times for these threads,
    #                                 and also last message texts
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserThreads, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['display_users'] = Book.objects.all()
        return context