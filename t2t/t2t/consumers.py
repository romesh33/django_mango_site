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
    # Extract the room from the message. This expects message.path to be of the
    # form /chat/{label}/, and finds a Room if the message path is applicable,
    # and if the Room exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    event_id = 0
    try:
        #print(message.user)
        #print(message['path'])
        thread_id = message['path'].strip('/').split('/')[3]
        group_name = 'chat-'+thread_id
        print("Group name:" + group_name)
        Group(group_name, channel_layer=message.channel_layer).add(message.reply_channel)
        #print(thread_id)
        # prefix, label = message['path'].decode('ascii').strip('/').split('/')
        # if prefix != 'chat':
        #     log.debug('invalid ws path=%s', message['path'])
        #     return
        #thread = MessageThread.objects.get(id=thread_id)
        #print(thread)
    except ValueError:
        #log.debug('invalid ws path=%s', message['path'])
        return
    except IndexError:
        event_id = message['path'].strip('/').split('/')[2]
        #print(event_id)
        group_name = 'multichat-'+event_id
        print("Group name:" + group_name)
        Group(group_name, channel_layer=message.channel_layer).add(message.reply_channel)
        print("Sending user name to socket: " + message.user.username)
        Group(group_name, channel_layer=message.channel_layer).send({'text': json.dumps({"user_connected": message.user.username})})
    # except Room.DoesNotExist:
    #     log.debug('ws room does not exist label=%s', label)
    #     return
    #
    # log.debug('chat connect room=%s client=%s:%s',
    #     room.label, message['client'][0], message['client'][1])
    #
    # # Need to be explicit about the channel layer so that testability works
    # # This may be a FIXME?
    #print(message.reply_channel)
    #Group('chat-'+thread_id, channel_layer=message.channel_layer).add(message.reply_channel)
    #
    # message.channel_session['room'] = room.label


@channel_session_user
def ws_receive(message):
    try:
        # если из пути можно вычленить thread_id, а значит, сообщение было послано из личной переписки:
        thread_id = message['path'].strip('/').split('/')[3]
        print("Sending personal message")
        send_personal_message(message, thread_id)
    except IndexError:
        # если из пути нельзя вычленить thread_id (оно было послано из чата события), получаем event_id:
        event_id = message['path'].strip('/').split('/')[2]
        print("Sending chat message")
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
    text = json.loads(message['text'])
    message_text = text["message"]
    sender = message.user
    event = get_object_or_404(Event,pk=event_id)
    new_chat_message = ChatMessage(sender=sender, text=message_text, event=event)
    new_chat_message.save()
    dt = datetime.datetime.now()
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", message_text)
        return
    if data:
        log.debug('chat message =%s', data['message'])
    print(message_text)
    group_name = 'multichat-'+event_id
    Group(group_name, channel_layer=message.channel_layer).send({'text': json.dumps({"message_text": message_text,
                                                        "sender": sender.username,
                                                        "creation_time": dt.strftime("%s %s" % ("%a %d %b %Y", "%H:%M"))})})