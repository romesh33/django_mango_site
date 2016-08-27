from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    from_user = models.ForeignKey(User, related_name="from_user")
    to_user = models.ForeignKey(User, related_name="to_user")
    text = models.TextField(max_length=2000, null=True, blank=True)
    def __str__(self):
        return self.text[0:10]