from django import forms
from .models import Setting, Page, Link, User

class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = ['setting']


class AddPageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'description', 'color', 'content']


class DelForm(forms.Form):
    field = forms.CharField(label='', max_length=30)


class DelFormPassword(forms.Form):
    field = forms.CharField(label='', max_length=30, widget=forms.PasswordInput)


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class CreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'name']
        widgets = {
            'password': forms.PasswordInput(),
        }


class ChangeNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
