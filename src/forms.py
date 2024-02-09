from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import *

class RegisterUserForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'email'      : forms.TextInput(attrs= {'class' : 'form-control'}),
            'first_name' : forms.TextInput(attrs = {'class':'form-control'}),
            'last_name'  : forms.TextInput(attrs = {'class':'form-control'}),    
            }

        labels ={
            'email': 'Email'
        }
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields =['first_name', 'last_name', 'phone' ]
        widgets ={
            'first_name' : forms.TextInput(attrs = {'class':'form-control'}),
            'last_name' : forms.TextInput(attrs = {'class':'form-control'}),
            'phone' : forms.NumberInput(attrs={'class':'form-control' , 'placeholder':'Phone'}),
        }        

## Content     
class AddContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['category', 'title', 'description', 'file', 'tags']
        
class TagForm(forms.Form):
    tag_id = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        empty_label="Select a Tag",
        label="Tag",
        widget=forms.Select(
            attrs={
                'class': 'form-control me-2 tag_id',
                'name': 'tag_id',
                'hx-get': '/filter-category/',
                'hx-trigger': 'change',
                'hx-target': '.cards-styles',
                'hx-swap': 'outerHTML',
            }
        ),
        required=True
    )



class CategoryForm(forms.Form):
    category_id = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a Category",
        label="Category",
        widget=forms.Select(
            attrs={
                'class': 'form-control me-2 category_id',
                'name': 'category_id',
                'hx-get': '/filter-category/',
                'hx-trigger': 'change',
                'hx-target': '.cards-styles',
                'hx-swap': 'outerHTML',
            }
        ),
        required=True
    )


   
