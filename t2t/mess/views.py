from django.http import HttpResponseRedirect
from django.views import generic
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
import logging
from django.contrib.auth.decorators import login_required
from .forms import NewMessageForm, ReplyMessageForm
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
            thread = MessageThread.objects.get_or_create_thread(from_user=user, to_user=to_user)
            #print(thread)
            message = Message(from_user=user, to_user=to_user, text=text, thread=thread)
            message.save()
            thread.last_message_id = message.id
            #print(message)
            # thread = message.thread
            # print(thread)
            thread_id = thread.id
            context = {"new_message_form": new_message_form, "message_status": 1}
            return HttpResponseRedirect(reverse('mess:view_thread', args=(thread_id,)), )
            #return render(request, 'mess/new_message.html', context)
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


@login_required()
def view_thread(request, thread_id):
    user = request.user
    thread_current = get_object_or_404(MessageThread,pk=thread_id)
    thread_users = thread_current.users.all()
    #print(thread_users)
    for u in thread_users:
        print(u.username)
        if u != user:
            companion_name = u.username
            break
    #print(companion_name)
    if thread_current.users.filter(username=user.username).exists():
        # если юзер хочет просмотреть переписку, в которой состоит - пожалуйста:
        messages = Message.objects.filter(thread=thread_current)
        context = {"thread_messages": messages, "companion_name": companion_name}
    else:
        # если юзер хочет посмотреть переписку, в которой не состоит - получает фигу:
        context = {"thread_messages": None, "companion_name": companion_name}
    reply_message_form = ReplyMessageForm()
    context["reply_message_form"] = reply_message_form
    context["thread_id"] = thread_id
    return render(request, 'mess/thread_messages.html', context)


@login_required()
def reply_message(request, thread_id):
    user = request.user
    thread = get_object_or_404(MessageThread,pk=thread_id)
    if request.method == 'POST':
        reply_message_form = ReplyMessageForm(data=request.POST)
        if reply_message_form.is_valid():
            from_user = user
            users = thread.users.all()
            for i in users:
                if i != from_user:
                    to_user = i
            text = request.POST['text']
            message = Message.objects.create_message(from_user=from_user, to_user=to_user, text=text)
            #message.save()
            view_thread(request, thread_id)
        else:
            print(reply_message_form.errors)
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    #reply_message_form = ReplyMessageForm()
    #thread_messages = MessageThread.objects.filter(pk=thread_id)
    #context = {"reply_message_form": reply_message_form, "thread_id": thread_id, "thread_messages": thread_messages}
    #return render(request, 'mess/thread_messages.html', context)
    return HttpResponseRedirect(reverse('mess:view_thread', args=(thread_id,)), )

@login_required()
def show_threads(request):
    user = request.user
    threads_to_display = []
    #Определям список тредов, в которых участвовал наш юзер:
    user_threads = MessageThread.objects.filter(users=user)
    #print(user_threads)
    #Перебираем список тредов в списке и заполняем список тредов для отображения:
    for user_thread in user_threads:
        if user_thread.num_of_users == 2:
            users = user_thread.users.all()
            for i in users:
                if i != user:
                    companion = i
            last_message_id = user_thread.last_message_id
            last_message = Message.objects.get(id=last_message_id)
            threads_to_display.append([companion.username,last_message.creation_time,last_message.text, user_thread.id])
            #users = users.exixts(user)
            #print(companion)
        else:
            # игнорируем треды, в которых больше двух юзеров - их мы не будем показывать
            pass
    #print(threads_to_display)
    context = {"threads_to_display": threads_to_display}
    return render(request, 'mess/user_threads.html', context)