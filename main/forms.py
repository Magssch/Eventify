from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

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
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.password1 = self.cleaned_data["password1"]
        user.password2 = self.cleaned_data["password2"]
        if commit:
            user.save()
        return user