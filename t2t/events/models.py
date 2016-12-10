from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, default="This is default event description")
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    max_participants_number = models.IntegerField(default=50)
    current_participants_number = models.IntegerField(default=0)
    users = models.ManyToManyField(User)
    online_chat_users = models.ManyToManyField(User, related_name="online_users")

    def __str__(self):
        return self.event_name
