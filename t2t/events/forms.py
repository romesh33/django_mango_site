from .models import Message
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