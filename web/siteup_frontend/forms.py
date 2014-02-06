#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from django.utils.translation import ugettext, ugettext_lazy as _

class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)

        # Add 'error' class to those widgets with errors
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    classes = self.fields[f_name].widget.attrs.get('class', '')
                    classes += ' error'
                    self.fields[f_name].widget.attrs['class'] = classes


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)

        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    classes = self.fields[f_name].widget.attrs.get('class', '')
                    classes += ' error'
                    self.fields[f_name].widget.attrs['class'] = classes


###################################################################################


class LoginForm(BaseForm):
    #error_css_class = 'errorcio'
    username = forms.CharField(label=_("Username"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def clean(self):
        super(BaseForm, self).clean()

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                self.user = authenticate(email=username, password=password)

            if self.user is None:
                raise forms.ValidationError(_("Invalid login"))
            elif not self.user.is_active:
                raise forms.ValidationError(_("This account is inactive."))

        return self.cleaned_data

    def get_user(self):
        return self.user


class SignupForm(BaseForm):
    username = forms.CharField(label=_("Username"), max_length=254)
    email = forms.CharField(label=_("Email"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

