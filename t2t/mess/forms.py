from .models import Message, ChatMessage
from django.contrib.auth.models import User
from django import forms


class NewMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('to_user', 'text')


class ReplyMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text',)


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ('text',)