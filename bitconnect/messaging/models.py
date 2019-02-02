from django.db import models
from django.contrib.auth.models import User
from base.models import Member
from django.utils import timezone

class Chat (models.Model) :
    members = models.ManyToManyField(Member , related_name='conversations' , symmetrical = False , related_query_name='members')
    last_message = models.DateTimeField(default = timezone.now)

class Messages (models.Model) :
    author = models.ForeignKey(Member , on_delete=models.CASCADE , related_name='messages' , unique = False)
    chat = models.ForeignKey(Chat , on_delete=models.CASCADE , related_name='messages' , unique = False)
    content = models.TextField()
    time = models.DateTimeField(default = timezone.now)
