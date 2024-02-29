from django import forms
from django.forms import DateInput
from .models import *

class PhotoForm(forms.ModelForm):
    date_phot = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = Photo
        fields = ('title','photo','date_phot')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ('namuser','body',)
        widgets = {
            'namuser': forms.TextInput(attrs={'class':'form-control',}),
            'body': forms.Textarea(attrs={'class':'form-control','rows':'5'}),
        }

class UpdatPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title','photo','date_phot')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'date_phot' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        } 
    def __init__(self, *args, **kwargs):
        super(UpdatPhotoForm, self).__init__(*args, **kwargs)
        self.fields["date_phot"].input_formats = ("%Y-%m-%d",)
    

class VideoForm(forms.ModelForm):
    date = forms.DateField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = Video
        fields = ('title','video','date')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
        }
        
class UpdatVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title','video','date')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'date' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        } 
    def __init__(self, *args, **kwargs):
        super(UpdatVideoForm, self).__init__(*args, **kwargs)
        self.fields["date"].input_formats = ("%Y-%m-%d",)       
        
         
class EvenementForm(forms.ModelForm):
    date_event = forms.DateField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = Evenement
        fields = ('auteur','title','image','text','date_event')
        widgets = {
            'auteur': forms.TextInput(attrs={'class':'form-control','value':'', 'id': 'elder','type':'hidden'}),
            #'auteur': forms.Select(attrs={'class':'form-control',}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'text': forms.Textarea(attrs={'class':'form-control','rows':'4'}),
            
        }

class UpdatEvenementForm(forms.ModelForm):
    date_event = forms.DateField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = Evenement
        fields = ('title','image','text','date_event')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'text': forms.Textarea(attrs={'class':'form-control','rows':'4'}),
            
        }
    def __init__(self, *args, **kwargs):
        super(UpdatEvenementForm, self).__init__(*args, **kwargs)
        self.fields["date_event"].input_formats = ("%Y-%m-%d",)