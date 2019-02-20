from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Event


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {
            'email',
            'first_name',
            'last_name'
        }


    field_order = [
        'first_name',
        'last_name',
        'email'
    ]

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = {
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        }

        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control', 'required':'required'}),
            'first_name':forms.TextInput(attrs={'class':'form-control', 'required':'required'}),
            'last_name':forms.TextInput(attrs={'class':'form-control', 'required':'required'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'required':'required'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control'}),
        }

    field_order = [
        'username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2',
    ]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['name', 'date', 'location', 'price', 'description']
