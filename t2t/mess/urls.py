from django.conf.urls import url

from . import views
from .views import UserMessages

app_name = 'mess'
urlpatterns = [
    # ex: /mess
    url(r'^$', views.view_messages_page, name='view_messages_page'),
    # ex: /mess/new/
    url(r'^new$', views.new_message_page, name='new_message_page'),
    # ex: /mess/send/
    url(r'^send$', views.new_message_page, name='new_message_page'),
    # ex: /mess/messages/
    url(r'^messages$', UserMessages.as_view(), name='messages_list'),
    # ex: /mess/threads/
    url(r'^threads/$', views.show_threads, name='show_threads'),
    # ex: /mess/threads/5/
    url(r'^threads/(?P<thread_id>[0-9]+)/$', views.view_thread, name='view_thread'),
    # ex: /mess/threads/5/reply
    url(r'^threads/(?P<thread_id>[0-9]+)/reply$', views.reply_message, name='reply_message'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # # ex: /polls/5/results/
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
