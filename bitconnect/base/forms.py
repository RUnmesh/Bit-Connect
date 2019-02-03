from django import forms
from .models import Post , Comments

class SignUpForm(forms.Form) :
    username = forms.CharField(max_length=200)
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    birth_date = forms.DateField(widget = forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices = ((1,'Male'),(2,'Female')) , widget=forms.RadioSelect)
    phone = forms.CharField(max_length=20)
    password = forms.CharField(widget = forms.PasswordInput)

class SignInForm(forms.Form) :
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget = forms.PasswordInput)

class CreatePostForm(forms.ModelForm):

    class Meta :
        model = Post
        fields = ['title' , 'content' ]

class CreateCommentForm(forms.ModelForm) :
    
    class Meta :
        model = Comments
        fields = ['content']

class EditProfForm (forms.Form) :
    bio = forms.CharField(widget = forms.Textarea)
