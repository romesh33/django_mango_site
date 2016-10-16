import re
import datetime
import json
import logging
from channels import Channel, Group
from channels.sessions import channel_session
from django.shortcuts import get_object_or_404
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
from mess.models import Message, MessageThread, ChatMessage
from events.models import Event
from channels.handler import AsgiRequest

log = logging.getLogger(__name__)

@channel_session_user_from_http
def ws_connect(message):
    event_id = 0
    try:
        thread_id = message['path'].strip('/').split('/')[3]
        group_name = 'chat-'+thread_id
        print("Group name:" + group_name)
        Group(group_name, channel_layer=message.channel_layer).add(message.reply_channel)
    except ValueError:
        return
    except IndexError:
        event_id = message['path'].strip('/').split('/')[2]
        group_name = 'multichat-'+event_id
        print("Group name:" + group_name)
        Group(group_name, channel_layer=message.channel_layer).add(message.reply_channel)
        print("Sending user name to socket: " + message.user.username)
        Group(group_name, channel_layer=message.channel_layer).send({'text': json.dumps({"user_connected": message.user.username})})

@channel_session_user
def ws_receive(message):
    try:
        # если из пути можно вычленить thread_id, а значит, сообщение было послано из личной переписки:
        print(message['path'].strip('/').split('/'))
        thread_id = message['path'].strip('/').split('/')[3]
        print("Sending personal message")
        send_personal_message(message, thread_id)
    except IndexError:
        # если из пути нельзя вычленить thread_id (оно было послано из чата события), получаем event_id:
        event_id = message['path'].strip('/').split('/')[2]
        print("Sending chat message to event ID: " + event_id)
        send_chat_message(message, event_id)

@channel_session_user_from_http
def ws_disconnect(message):
    #print(message)
    #print(message.reply_channel)
    #print(message.user)
    try:
        thread_id = message['path'].strip('/').split('/')[3]
        #     label = message.channel_session['room']
        #     room = Room.objects.get(label=label)
        group_name = 'chat-'+thread_id
        Group(group_name, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError):
        pass
    except IndexError:
        event_id = message['path'].strip('/').split('/')[2]
        #print(event_id)
        group_name = 'multichat-'+event_id
        Group(group_name, channel_layer=message.channel_layer).discard(message.reply_channel)

def send_personal_message(message, thread_id):
    text = json.loads(message['text'])
    message_text = text["message"]
    from_user = message.user
    thread = MessageThread.objects.get(id=thread_id)
    for u in thread.users.all():
        if u != from_user:
            to_user = u
    thread = MessageThread.objects.get_or_create_thread(from_user=from_user, to_user=to_user)
    new_message = Message(from_user=from_user, to_user=to_user, text=message_text, thread=thread)
    new_message.save()
    thread.last_message_id = new_message.id
    thread.save()
    dt = datetime.datetime.now()
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", message_text)
        return
    if data:
        log.debug('chat message =%s', data['message'])
    group_name = 'chat-'+thread_id
    Group(group_name, channel_layer=message.channel_layer).send({'text': json.dumps({"message_text": message_text,
                                                        "from_user": from_user.username,
                                                        "to_user": to_user.username,
                                                        "creation_time": dt.strftime("%s %s" % ("%a %d %b %Y", "%H:%M"))})})


def send_chat_message(message, event_id):
    text = message['text']
    print("path = " + message['path'])
    print("text = " + text)
    sender = message.user
    print("sender = " + sender.username)
    event = get_object_or_404(Event,pk=event_id)
    new_chat_message = ChatMessage(sender=sender, text=text, event=event)
    new_chat_message.save()
    dt = datetime.datetime.now()
    time = dt.strftime("%s %s" % ("%a %d %b %Y", "%H:%M"))
    print("time = " + time)
    group_name = 'multichat-'+event_id
    #data_to_send = {'content': json.dumps({"message_text": text, "from": sender.username, "time": time})}
    print("Sending message in consumer to group name: " + group_name)
    #print(data_to_send)
    Group(group_name, channel_layer=message.channel_layer).send({'text': json.dumps({"message_text": text,
                                                                                     "sender": sender.username,
                                                                                     "time": time})})
    print("Sent")