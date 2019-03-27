from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from newsletter.models import Message, Submission, Article, Subscription
from .models import Event

# Form for editing user attributes
class EditUserForm(forms.ModelForm):
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

# User registration form
class RegistrationForm(UserCreationForm):

    check = forms.BooleanField(required = True, label="I accept the Eventify terms of use and privacy policy")

    class Meta:
        model = User
        fields = {
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        }

        widget = {
            'username':forms.TextInput(attrs={'class':'form-control', 'required':'required'}),
            'first_name':forms.TextInput(attrs={'class':'form-control', 'required':'required'}),
            'last_name':forms.TextInput(attrs={'class':'form-control', 'required':'required'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'required':'required'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control'})
        }

    field_order = [
        'username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2'
    ]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# Form for events
class EventForm(forms.ModelForm):
    name = forms.CharField(
                                    label='Name of the event:',
                                    widget=forms.TextInput(attrs={"placeholder": "Enter event name"})
    )
    location = forms.CharField(     label='Location:', widget=forms.TextInput(attrs={"placeholder": "London, New York, etc."}))
    price = forms.IntegerField(     label='Price of the event:', initial=250)
    description = forms.CharField(
                                    label='Description of the event, not required',
                                    widget=forms.Textarea()
    )
    capacity = forms.IntegerField(  label='Maximum number of attendees', initial=100)
    date = forms.DateField(         required    = False,
                                    widget      = forms.DateInput(format=('%m/%d/%Y'),
                                    attrs={'id':'date1', 'placeholder':'Select a date'}),
                                    input_formats=('%m/%d/%Y', )
    )
    registration_starts = forms.DateField(
                                    required    = False,
                                    widget      = forms.DateInput(format=('%m/%d/%Y'),
                                    attrs={'id':'date2', 'placeholder':'Select a date'}),
                                    input_formats=('%m/%d/%Y', )
    )
    image = forms.FileField()

    class Meta:
        model = Event
        fields = [
            'name',
            'location',
            'price',
            'capacity',
            'description',
            'date',
            'registration_starts',
            'image',
        ]
        widget = {}

class MessagingForm(forms.ModelForm):
    title = forms.CharField(        label="Message title", 
                                    widget =forms.TextInput(attrs={"placeholder": "Enter your message title"}))
    # We might need the foreign key to newsletter?
    # newsletter = forms.foreign
    class Meta:
        model = Message
        fields = [
            'title'
        ]

class ArticleForm(forms.ModelForm):
    text = forms.CharField(
                                    label       = 'Message',
                                    widget      = forms.Textarea(attrs={'rows': '100','cols': '60','style': 'height: 15em;'}),
                                )
    class Meta:
        model = Article
        fields = [
            'text'
        ]

class SubscribeNewsletterForm(forms.ModelForm):
    subscribed = forms.BooleanField(required=False, initial=False, label="I'd like to subscribe to Eventify's newsletter")

    class Meta:
        model = Subscription
        fields = [
            'subscribed'
        ]