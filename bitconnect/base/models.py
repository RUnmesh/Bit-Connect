from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

def path_and_rename(instance, filename):
    upload_to = 'profile_pics'
    filename = instance.username
    return os.path.join(upload_to, filename)

class Member(models.Model) :
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    birth_date = models.DateField()
    phone = models.CharField(max_length=20)
    gender = models.IntegerField()
    friends = models.ManyToManyField("self" , related_name='friends' , symmetrical=True , blank = True)
    friend_requests = models.ManyToManyField("self" , related_name = 'sent_requests' , symmetrical = False , blank = True)
    last_seen = models.DateTimeField(default = timezone.now)
    online = models.BooleanField(default = False)
    last_message = models.DateTimeField(default = timezone.now)
    profile_pic = models.ImageField(upload_to = path_and_rename , blank = True , null = True)
    bio = models.TextField(null = True , blank = True)

    def __str__(self) :
        return self.username

class Post(models.Model) :
    time = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(Member , on_delete=models.CASCADE , related_name='posts')
    title = models.CharField(max_length = 300)
    content = models.TextField()
    liked = models.ManyToManyField(Member , related_name='liked' , symmetrical= False , blank = True)

    def __str__(self) :
        return self.title

class Comments(models.Model) :
    time = models.DateTimeField(default = timezone.now)
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='comments')
    author = models.ForeignKey(Member , on_delete=models.CASCADE )
    content = models.TextField()



