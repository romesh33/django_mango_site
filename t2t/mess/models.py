from django.db import models
from django.contrib.auth.models import User
from events.models import Event

class ThreadManager(models.Manager):
     # Проверяем, есть ли цепочка сообщений, в которой есть оба юзера и число юзеров в которой равна 2:
    def get_or_create_thread(self, from_user, to_user):
        # Проверяем, есть ли цепочка сообщений, в которой есть оба юзера и число юзеров в которой равна 2:
        query_set = MessageThread.objects.filter(users=from_user).filter(users=to_user)
        if len(query_set) != 0:
            for thread in query_set:
                if thread.num_of_users == 2:
                    return thread
        else:
            users = [from_user, to_user]
            num_of_users = len(users)
            thread = MessageThread()
            thread.save()
            for user in users:
                thread.users.add(user)
            thread.num_of_users = num_of_users
            thread.save()
            return thread


# Create your models here.
class MessageThread(models.Model):
    users = models.ManyToManyField(User, default=None, null=True)
    num_of_messages = models.IntegerField(default=0)
    num_of_users = models.IntegerField(default=0)
    last_message_id = models.IntegerField(default=0)
    objects = ThreadManager()


class Message(models.Model):
    from_user = models.ForeignKey(User, related_name="from_user")
    to_user = models.ForeignKey(User, related_name="to_user")
    thread = models.ForeignKey(MessageThread, null=True)
    text = models.TextField(max_length=2000, null=True, blank=True)
    creation_time = models.DateTimeField('creation time', auto_now=True)
    #objects = MessageManager()

    def __str__(self):
        if self.text:
            return self.text[0:10]
        else:
            return "Message text is empty"


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sender")
    event = models.ForeignKey(Event, related_name="event")
    text = models.TextField(max_length=2000, null=True, blank=True)
    creation_time = models.DateTimeField('creation time', auto_now=True)
    is_deleted = models.BooleanField(default=False)
    #objects = MessageManager()

    def __str__(self):
        if self.text:
            return self.text[0:10]
        else:
            return "Message text is empty"