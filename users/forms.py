from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from users.models import userAccount

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text = "Required: Please Add a valid email ")
    
    class Meta:
        model = userAccount
        fields = ('username','email','gender','password1','password2', 'gender', 'user_DOB','Address','phone_number')

    #function to clean the email to lower_case before submitting in Database
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            #looking into account for search crieteria, get will fetch single rec
            account = userAccount.objects.exclude(pk=self.instance.pk).get(email=email)
        except userAccount.DoesNotExist:
            return email
        raise forms.ValidationError(f"Email {email} is already in use")

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            #looking into account for search crieteria, get will fetch single rec
            account = userAccount.objects.get(username= username)
        except userAccount.DoesNotExist:
            return username
        raise forms.ValidationError(f"username {username} is already in use")
