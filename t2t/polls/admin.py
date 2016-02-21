from django.contrib import admin

from .models import Question, Event, Participant

admin.site.register(Question)
admin.site.register(Event)
admin.site.register(Participant)
