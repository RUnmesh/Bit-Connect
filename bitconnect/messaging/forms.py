from django import forms
from .models import Messages

class CreateMessage (forms.ModelForm) :

    class Meta :
        model = Messages
        fields = ['content']