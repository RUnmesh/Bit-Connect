from django.db import models
from django.contrib.auth.models import User
from base.models import Member

class Chat (models.Model) :
    members = models.ManyToManyField(Member , related_name='conversations' , symmetrical = False)
    group = models.BooleanField(default = False)

class Messages (models.Model) :
    author = models.ForeignKey(Member , on_delete=models.CASCADE , related_name='messages')
    chat = models.ForeignKey(Chat , on_delete=models.CASCADE , related_name='messages')
    content = models.TextField()
