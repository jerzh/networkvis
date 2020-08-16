from django import forms
from .models import Setting, Page, Link, User


# form to set setting (determines which network is displayed)
class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = ['setting']


# form to add page (appears when '+' button on node is clicked)
class AddPageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'description', 'color', 'content']


# general delete confirmation form
class DelForm(forms.Form):
    field = forms.CharField(label='', max_length=30)


# general delete confirmation form with password
class DelFormPassword(forms.Form):
    field = forms.CharField(label='', max_length=30, widget=forms.PasswordInput)


# login form
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


# create new user form
class CreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'name']
        widgets = {
            'password': forms.PasswordInput(),
        }


# change display name form
class ChangeNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name']


# change password form (have to input old password as well)
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=100, widget=forms.PasswordInput)


# add link form (deprecated)
# class AddLinkForm(forms.ModelForm):
#     class Meta:
#         model = Link
#         fields = ['source', 'target', 'color']
