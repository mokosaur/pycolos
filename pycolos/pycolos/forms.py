from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _


class UserForm(forms.ModelForm):
    """Form that can be used to create a user without the requirement of a password confirmation"""
    group = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), label=_('Group'))
    password = forms.CharField(widget=forms.PasswordInput(), label=_('Password'))

    class Meta:
        model = User
        fields = ['username', 'password']
