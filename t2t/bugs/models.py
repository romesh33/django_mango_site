from django.db import models
from django.contrib.auth.models import User
from events.models import Event
import datetime
from django.utils import timezone
import logging

class TicketManager(models.Manager):
    def create_ticket(self, title, description, creator, ticket_type, event):
        ticket = self.create(title=title, description=description, creator=creator, ticket_type=ticket_type,
                             event=event)
        ticket.watchers.add(creator)
        return ticket


# Create your models here.
class Ticket(models.Model):
    title = models.CharField(max_length=200, default="Саммари по умолчанию", blank=False)
    description = models.TextField(max_length=2000, null=True, blank=True)
    creation_time = models.DateTimeField('creation time', auto_now=True)
    creator = models.ForeignKey(User, related_name="creators")
    TICKET_TYPE_CHOICES = (
        ('Баг', 'Баг'),
        ('Отчет', 'Отчет'),
    )
    ticket_type = models.CharField(max_length=5,
                                      choices=TICKET_TYPE_CHOICES,
                                      default='Баг')
    watchers = models.ManyToManyField(User, related_name="watchers", default=None, null=True)
    reviewers = models.ManyToManyField(User, related_name="reviewers", default=None, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    objects = TicketManager()

    # TODO: Need to create attachment model:
    # attachments = models.ManyToManyField(Attachment)
    # TODO: Need to add state: Closed, NotClosed, Reviewed, Not reviewed, etc
    def __str__(self):
        return self.title
