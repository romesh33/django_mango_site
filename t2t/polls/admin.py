from django.contrib import admin

from .models import Question, Event, Choice, Participant

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Event)
admin.site.register(Participant)
