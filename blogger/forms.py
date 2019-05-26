from django import forms
from .models import Setting, Page

class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = ['setting']

class AddPageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'description', 'color', 'content']

class DelPageForm(forms.Form):
    title = forms.CharField(label='', max_length=30)
