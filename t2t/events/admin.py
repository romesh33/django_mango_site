from django.contrib import admin
from .models import Participant, Event

# Register your models here.
admin.site.register(Event)
admin.site.register(Participant)