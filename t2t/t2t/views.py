from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render

#from .models import Question

def main(request):
    return render(request, 'polls/jumbotron.html', {})
	
def contacts(request):
    return render(request, 'polls/contacts.html', {})