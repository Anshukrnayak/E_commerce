from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']
    
    def __init__(self,*args,**kwargs):
        super(SignupForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class']='form-control border-primary'
        self.fields['password1'].widget.attrs['class']='form-control border-primary'
        self.fields['password2'].widget.attrs['class']='form-control border-primary'