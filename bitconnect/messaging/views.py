from django.shortcuts import render , redirect
from .models import Chat , Messages
from base.models import Member
from django.contrib.auth.models import User
from .forms import CreateMessage
from django.contrib.auth.decorators import login_required
from operator import attrgetter
from django.utils import timezone

@login_required(login_url='/')
def index (request) :
    user = request.user
    current_member = Member.objects.get(user = user)
    chats = [chat for chat in current_member.conversations.all()]
    newposs = [mem for mem in current_member.friends.all()]
    for chat in chats :
        if (chat.messages.count() == 0) :
            chats.remove(chat)
        else :
            for member in chat.members.all() :
                if (member.user != current_member.user) and (member in current_member.friends.all()) :
                    newposs.remove(member)
    sortedchats  = sorted(chats , key = attrgetter('last_message') , reverse = True)
    context = {
        'current_member' : current_member ,
        'member' : current_member ,
        'chats' : sortedchats ,
        'newconvos' : newposs ,
    }
    return render(request , 'messaging/index.html' , context)

def getconvo (request , mem_id) :
    user = request.user
    current_member = Member.objects.get(user = user)
    member = Member.objects.get(pk = mem_id)
    chat = None
    for convo in Chat.objects.all() :
        if (current_member in convo.members.all()) and (member in convo.members.all()):
            chat = convo
    if chat == None :
        chat = Chat.objects.create()
        chat.members.add(current_member)
        chat.members.add(member)
        chat.save()
    return chat

@login_required(login_url='/')
def message (request , mem_id) :
    chat = getconvo(request , mem_id)
    user = request.user
    current_member = Member.objects.get(user = user)
    member = Member.objects.get(pk = mem_id)
    if request.method == "POST" :
        form = CreateMessage(request.POST)
        message = form.save(commit = False)
        message.author = current_member
        message.chat = chat
        chat.last_message = timezone.now()
        chat.save()
        message.save()
        return redirect('messaging:message' , mem_id = mem_id)
    else :
        form = CreateMessage()
        context = {
        'current_member' : current_member ,
        'member' : member ,
        'chat' : chat ,
        'form' : form ,
        }
        return render(request , 'messaging/chat.html' , context)


