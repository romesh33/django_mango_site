from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_length=200)
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    max_participants_number = models.IntegerField(default=50)

    def __str__(self):
        return self.event_name


class Participant(models.Model):
    user_id = models.ForeignKey(User)
    event_id = models.ForeignKey(Event)

    def __str__(self):
        return "This is just the link between User object and Event"
