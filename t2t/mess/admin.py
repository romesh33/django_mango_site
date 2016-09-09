from django.contrib import admin

from .models import Message,ChatMessage,MessageThread

# Register your models here.
admin.site.register(Message)
admin.site.register(ChatMessage)
admin.site.register(MessageThread)