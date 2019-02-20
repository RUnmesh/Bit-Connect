from django.shortcuts import render
from .forms import SignUpForm , SignInForm , CreatePostForm , CreateCommentForm , EditProfForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from .models import Member , Post ,Comments , Sessions
from django.contrib.auth import authenticate , login , logout
from django.utils import timezone
from operator import attrgetter
from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index (request) :
    recent_users = []
    if 'id' in request.COOKIES:
        sess = Sessions.objects.get(pk = int(request.COOKIES['id']))
        recent_users = [user for user in sess.users.all()]
    if request.method == 'POST' :
        form = SignUpForm(request.POST)
        if form.is_valid() :
            user_name = request.POST.get('username')
            passw = request.POST.get('password')
            user = User.objects.create_user(username=user_name , password=passw)
            user.save()
            fn = request.POST.get('first_name')
            ln = request.POST.get('last_name')
            phone = request.POST.get('phone')
            bd = request.POST.get('birth_date')
            em = request.POST.get('email')
            gender = int(request.POST.get('gender'))
            mem = Member(username =user_name , user = user , first_name = fn , last_name = ln , phone = phone , birth_date = bd , email = em , gender = gender)
            mem.save()
            messages.success(request , "Account created")
            return redirect('signin')
        else:
            form = SignUpForm()
            messages.error(request , "Check details")
            return render(request , 'base/index.html' , {'form':form , 'recent_users' : recent_users[-4:]})            
    else :
        form = SignUpForm()
        resp = render(request , 'base/index.html' , {'form':form , 'recent_users' : recent_users[-4:]})
        if 'id' not in request.COOKIES:
            sess = Sessions.objects.create()
            resp.set_cookie('id' , sess.id)
        return resp

def signin (request) :
    if request.method == 'POST' :
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = user_name , password = password)
        if user :
            login(request , user)
            member = Member.objects.get(user = user)
            member.online = True
            member.save()
            sess = Sessions.objects.get(pk = int(request.COOKIES['id']))
            if member not in sess.users.all():
                sess.users.add(member)
                if sess.users.all().count() > 4:
                    u = [user for user in sess.users.all()]
                    sess.users.remove(u[0])
                sess.save()
            return redirect('myposts' , mem_id = member.id)
        else :
            messages.error(request , "Please check your login credentials")
            return redirect('signin')

    else :
        form = SignInForm()
        return render(request , 'base/signin.html' , {'form':form})

@login_required(login_url='/')
def logouts (request) :
    user = request.user
    current_member = Member.objects.get(user = user)
    current_member.last_seen = timezone.now()
    current_member.online = False
    current_member.save()
    logout(request)
    messages.success(request , "Logged out successfully")
    return redirect('signin')

def unfriend (request , mem_id) :
    user = request.user
    member_viewed = Member.objects.get(pk = mem_id)
    current_member = Member.objects.get(user = user)
    current_member.friends.remove(member_viewed)
    member_viewed.friends.remove(current_member)
    return redirect('myposts' , mem_id = mem_id)

def mainunfriend (request , mem_id) :
    user = request.user
    member_viewed = Member.objects.get(pk = mem_id)
    current_member = Member.objects.get(user = user)
    current_member.friends.remove(member_viewed)
    member_viewed.friends.remove(current_member)
    return redirect('friends')

@login_required(login_url='/')
def my_posts(request , mem_id) :
    user = request.user
    member= Member.objects.get(pk = mem_id)
    current_member = Member.objects.get(user = user)
    if request.method == "POST" :
        form = CreatePostForm(request.POST)
        post = form.save(commit = False)
        post.author = current_member
        post.time = timezone.now()
        post.save()
        return redirect('myposts' , mem_id = current_member.id)
    else :
        form =  CreatePostForm()
        context = {
            'member' : member ,
            'current_member' : current_member , 
            'form' : form
        }
        return render(request , 'base/mypost.html' , context)

@csrf_exempt
def likes (request) :
    post = Post.objects.get(pk = int(request.POST.get('post')))
    user = request.user
    current_member = Member.objects.get(user = user)
    post.liked.add(current_member)
    data = {'likes' : post.liked.all().count()}
    return JsonResponse(data)

@csrf_exempt
def dislikes (request) :
    post = Post.objects.get(pk = int(request.POST.get('post')))
    user = request.user
    current_member = Member.objects.get(user = user)
    post.liked.remove(current_member)
    data = {'likes' : post.liked.all().count()}
    return JsonResponse(data)

@login_required(login_url='/')
def posts (request) :
    user = request.user
    current_member = Member.objects.get(user = user)
    post=[]
    for friend in current_member.friends.all() :
        for p in friend.posts.all() :
            post.append(p)
    number = len(post)
    ordered_post = sorted(post , key = attrgetter('time') , reverse = True)
    context = {
        'member' : current_member ,
        'current_member' : current_member , 
        'posts' : ordered_post ,
        'len' : number ,
    }
    return render(request , 'base/post.html' , context)

@login_required(login_url='/')
def postdetail (request , post_id) :
    post = Post.objects.get(pk = post_id)
    user = request.user
    current_member = Member.objects.get(user = user)
    if request.method == 'POST' :
        form = CreateCommentForm(request.POST)
        comment = form.save(commit = False)
        comment.author = current_member
        comment.time = timezone.now()
        comment.post = post
        comment.save()
        return redirect('postdetail' , post_id = post.id)
    else :
        form = CreateCommentForm()
        context = {
            'post' : post ,
            'current_member' : current_member ,
            'form' : form ,
        }
        return render(request , 'base/postdetail.html' , context)

@login_required(login_url='/')
def editpost (request , post_id) :
    post = Post.objects.get(pk = post_id)
    user = request.user
    current_member = Member.objects.get(user = user)
    if request.method == 'POST' :
        form = CreatePostForm(request.POST)
        new_post = form.save(commit = False)
        post.title = new_post.title
        post.content = new_post.content
        post.save()
        return redirect('myposts' , mem_id = current_member.id)
    else :
        form = CreatePostForm(instance = post)
        context = {
            'post' : post ,
            'current_member' : current_member ,
            'member' : current_member ,
            'form' : form ,
        }
        return render (request , 'base/editpost.html' , context)

def commentdelete (request , comment_id) :
    comment = Comments.objects.get(pk = comment_id)
    post_id = comment.post.pk
    comment.delete()
    return redirect('postdetail' , post_id = post_id)

@login_required(login_url='/')
def delete (request , post_id) :
    post = Post.objects.get(pk = post_id)
    post.delete()
    user = request.user
    current_member = Member.objects.get(user = user)
    return redirect('myposts' , mem_id = current_member.id)

@login_required(login_url='/')
def friends (request) :
    user = request.user
    current_member = Member.objects.get(user = user)
    context = {
        'current_member' : current_member ,
        'member' : current_member ,
    }
    return render(request , 'base/friends.html' , context)

@login_required(login_url='/')
def friendrequests (request) :
    user = request.user
    current_member = Member.objects.get(user = user)
    context = {
        'current_member' : current_member ,
        'member' : current_member ,
    }
    return render(request , 'base/friendrequests.html' , context)  

@login_required(login_url='/')
def acceptrequest (request , mem_id) :
    user = request.user
    member = Member.objects.get(pk = mem_id)
    current_member = Member.objects.get(user = user)
    current_member.friends.add(member)
    member.friends.add(current_member)
    current_member.friend_requests.remove(member)

@login_required(login_url='/')
def sendrequest (request , mem_id) :
    user = request.user
    member = Member.objects.get(pk = mem_id)
    current_member = Member.objects.get(user = user)
    member.friend_requests.add(current_member)

@login_required(login_url='/')
def deleterequest (request , mem_id) :
    user = request.user
    member = Member.objects.get(pk = mem_id)
    current_member = Member.objects.get(user = user)
    member.friend_requests.remove(current_member)

@login_required(login_url='/')
def rejectrequest (request , mem_id) :
    user = request.user
    member = Member.objects.get(pk = mem_id)
    current_member = Member.objects.get(user = user)
    current_member.friend_requests.remove(member)

def profacceptrequest (request , mem_id) :
    acceptrequest(request , mem_id)
    return redirect ('myposts' , mem_id = mem_id)

def profsendrequest (request , mem_id) :
    sendrequest(request , mem_id)
    return redirect ('myposts' , mem_id = mem_id)

def profdeleterequest (request , mem_id) :
    deleterequest(request , mem_id)
    return redirect ('myposts' , mem_id = mem_id)

def profrejectrequest (request , mem_id) :
    rejectrequest(request , mem_id)
    return redirect ('myposts' , mem_id = mem_id)

def reqacceptrequest (request , mem_id) :
    acceptrequest(request , mem_id)
    return redirect ('friendrequests')

def reqrejectrequest (request , mem_id) :
    rejectrequest(request , mem_id)
    return redirect ('friendrequests')

def reqdeleterequest (request , mem_id) :
    deleterequest(request , mem_id)
    return redirect ('friendrequests')

def frideleterequest (request , mem_id) :
    deleterequest(request , mem_id)
    return redirect ('friends')

def findacceptrequest (request , mem_id) :
    acceptrequest(request , mem_id)
    return redirect ('findpeople')

def findsendrequest (request , mem_id) :
    sendrequest(request , mem_id)
    return redirect ('findpeople')

def finddeleterequest (request , mem_id) :
    deleterequest(request , mem_id)
    return redirect ('findpeople')

def findrejectrequest (request , mem_id) :
    rejectrequest(request , mem_id)
    return redirect ('findpeople')

def find (request) :
    users = []
    user = request.user
    current_member = Member.objects.get(user = user)
    for member in Member.objects.all() :
        if (member!=current_member) and (member not in current_member.friends.all()) :
            users.append(member)
    context = {
        'current_member' : current_member ,
        'member' : current_member ,
        'users' : users ,
        }
    return render(request , 'base/findpeople.html' , context)

def prof_pic (request) :
    user = request.user
    current_member = Member.objects.get(user = user)
    context = {
        'current_member' : current_member ,
        'member' : current_member ,
        }
    if request.method == "POST" :
        image = request.FILES['profile_pic'] if 'profile_pic' in request.FILES else None
        if image != None :
            if current_member.profile_pic :
                current_member.profile_pic.delete()
            current_member.profile_pic = image
            current_member.save()
            return redirect('myposts' , current_member.id)

    return render(request , 'base/addprofpic.html' , context)

def editbio (request) :
    user = request.user
    current_member = Member.objects.get(user = user)
    if request.method == 'POST' :
        bio = request.POST.get('bio') if 'bio' in request.POST else None
        if bio != None :
            current_member.bio = bio
            current_member.save()
        else :
            return redirect('editbio')
        return redirect('myposts' , current_member.id)
    else :
        if current_member.bio != None :
            form = EditProfForm(initial = {'bio' : current_member.bio})
        else :
            form = EditProfForm()
        context = {
        'current_member' : current_member ,
        'member' : current_member ,
        'form' : form
        }
        return render(request , 'base/editbio.html' , context)



