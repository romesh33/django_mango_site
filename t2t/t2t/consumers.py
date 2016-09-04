import re
import datetime
import json
import logging
from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
from mess.models import Message, MessageThread
from channels.handler import AsgiRequest

log = logging.getLogger(__name__)

@channel_session_user_from_http
def ws_connect(message):
    # Extract the room from the message. This expects message.path to be of the
    # form /chat/{label}/, and finds a Room if the message path is applicable,
    # and if the Room exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    try:
        print(message.user)
        print(message['path'])
        thread_id = message['path'].strip('/').split('/')[3]
        #print(thread_id)
        # prefix, label = message['path'].decode('ascii').strip('/').split('/')
        # if prefix != 'chat':
        #     log.debug('invalid ws path=%s', message['path'])
        #     return
        thread = MessageThread.objects.get(id=thread_id)
        print(thread)
    except ValueError:
        #log.debug('invalid ws path=%s', message['path'])
        return
    # except Room.DoesNotExist:
    #     log.debug('ws room does not exist label=%s', label)
    #     return
    #
    # log.debug('chat connect room=%s client=%s:%s',
    #     room.label, message['client'][0], message['client'][1])
    #
    # # Need to be explicit about the channel layer so that testability works
    # # This may be a FIXME?
    print(message.reply_channel)
    Group('chat-'+thread_id, channel_layer=message.channel_layer).add(message.reply_channel)
    #
    # message.channel_session['room'] = room.label


@channel_session_user
def ws_receive(message):
    thread_id = message['path'].strip('/').split('/')[3]
    text = json.loads(message['text'])
    message_text = text["message"]
    from_user = message.user
    #print(message_text)
    thread = MessageThread.objects.get(id=thread_id)
    #print(message.reply_channel)
    #print(message.user)
    #request = AsgiRequest(message)
    #print(request)
    for u in thread.users.all():
        if u != from_user:
            to_user = u
    thread = MessageThread.objects.get_or_create_thread(from_user=from_user, to_user=to_user)
    new_message = Message(from_user=from_user, to_user=to_user, text=message_text, thread=thread)
    new_message.save()
    thread.last_message_id = new_message.id
    dt = new_message.creation_time
    #print(dt)
    #print(dt.strftime("%s %s" % ("%Y %m %d", "%H:%M:%S")))
    #creation_time = datetime.strftime("%s %s" % ("%Y %m %d", "%H:%M:%S"))
    #message = Message.objects.create_message(from_user=from_user, to_user=to_user, text=text)
    # Look up the room from the channel session, bailing if it doesn't exist
    # try:
    #     label = message.channel_session['room']
    #     room = Room.objects.get(label=label)
    # except KeyError:
    #     log.debug('no room in channel_session')
    #     return
    # except Room.DoesNotExist:
    #     log.debug('recieved message, buy room does not exist label=%s', label)
    #     return
    #
    # # Parse out a chat message from the content text, bailing if it doesn't
    # # conform to the expected message format.
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", message_text)
        return

    # if set(data.keys()) != set(('message')):
    #     log.debug("ws message unexpected format data=%s", data)
    #     return

    if data:
        log.debug('chat message =%s', data['message'])
    #     m = room.messages.create(**data)
    #
    ## See above for the note about Group
    #Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})
    Group('chat-'+thread_id, channel_layer=message.channel_layer).send({'text': json.dumps({"message_text": message_text,
                                                            "from_user": from_user.username,
                                                            "to_user": to_user.username,
                                                            "creation_time": dt.strftime("%s %s" % ("%a %d %b %Y", "%H:%M"))})})


@channel_session_user_from_http
def ws_disconnect(message):
    print(message)
    print(message.reply_channel)
    print(message.user)
    try:
        thread_id = message['path'].strip('/').split('/')[3]
        #     label = message.channel_session['room']
        #     room = Room.objects.get(label=label)
        Group('chat-'+thread_id, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError):
        pass
