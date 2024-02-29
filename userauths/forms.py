from collections.abc import Mapping
from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from userauths.models import User, UserProfile
from .models import GENDER_SELECTION

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"username",'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"email",'class':'form-control'}))
    gender = forms.ChoiceField(choices=GENDER_SELECTION, widget=forms.Select(attrs={"placeholder": "gender", 'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"password",'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm password",'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','email','gender','password1','password2']

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"type":"password",'class':'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"type":"password",'class':'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"type":"password",'class':'form-control'}))
    class Meta:
        model = User
        fields = ['old_password','new_password1','new_password2']
 
class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('gender','profile_pic','profession','commune')
        widgets = {
            'gender' : forms.Select(choices=GENDER_SELECTION,attrs={'class': 'form-control'}),
            'profession' : forms.TextInput(attrs={'class':'form-control'}),
            'commune': forms.TextInput(attrs={'class':'form-control'}),
           
        } 
    def __init__(self, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)
        self.fields["commune"].widget.attrs['class']='form-control'
        self.fields["profession"].widget.attrs['class']='form-control'
           
class UserProfilForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"username",'class':'form-control','disabled': 'disabled'}))
    profession = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"username",'class':'form-control','disabled': 'disabled'}))
    commune = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"username",'class':'form-control','disabled': 'disabled'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"email",'class':'form-control','disabled': 'disabled'}))
    gender = forms.ChoiceField(choices=GENDER_SELECTION, widget=forms.Select(attrs={"placeholder": "gender", 'class': 'form-control','disabled': 'disabled'}))
    class Meta:
        model = UserProfile
        fields = ['username','commune','email','gender','profession']
        
class CreateUserProfileForm(forms.ModelForm):
    profession = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    commune = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    gender = forms.ChoiceField(choices=GENDER_SELECTION, widget=forms.Select(attrs={"placeholder": "gender",'class':'form-control'}))
    class Meta:
        model = UserProfile
        fields = ('profession', 'commune', 'gender', 'profile_pic')
        




