from .models import Ticket
from django.contrib.auth.models import User
from django import forms


class NewTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'ticket_type')