from django import forms
from django.contrib.auth.models import User
from .models import *


class SignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        uname = self.cleaned_data["username"]
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "User with this user name already exists")
        return uname

    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        c_pword = self.cleaned_data["confirm_password"]
        if password != c_pword:
            raise forms.ValidationError("Password did not match")
        return c_pword


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "image", "content"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(widget=forms.PasswordInput())

    def clean_confirm_new_password(self):
        np = self.cleaned_data["new_password"]
        cnp = self.cleaned_data["confirm_new_password"]
        if np != cnp:
            raise forms.ValidationError("Passwords did not match")
        return cnp
