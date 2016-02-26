from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
	    return self.question_text
    def was_published_recently(self):
	    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
	
    def __str__(self):
	    return self.choice_text
		
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
		
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username
