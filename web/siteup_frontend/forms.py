#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
oplogger = logging.getLogger("operations")

from django import forms

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from django.utils.translation import ugettext, ugettext_lazy as _

from siteup_api import models

class BaseForm(forms.Form):
    """Base form class that adds a '.error' class to input widgets"""

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)

        # Add 'error' class to those widgets with errors
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    classes = [self.fields[f_name].widget.attrs.get('class', ''), "error"]
                    self.fields[f_name].widget.attrs['class'] = ' '.join(filter(None, classes))


class BaseModelForm(forms.ModelForm):
    """Base model form class that adds a '.error' class to input widgets"""

    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)

        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    classes = [self.fields[f_name].widget.attrs.get('class', ''), "error"]
                    self.fields[f_name].widget.attrs['class'] = ' '.join(filter(None, classes))


###################################################################################


class LoginForm(BaseForm):
    """
    Form for the login process. Tries to login with both the username and email.
    """

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
    """
    Form for the signup process. Checks if the username already exists.
    """

    username = forms.CharField(label=_("Username"), max_length=254)
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def clean(self):
        try:
            User.objects.get(username=self.cleaned_data.get('username'))
            raise forms.ValidationError(_("Username is already taken"))
        except User.DoesNotExist, e:
            pass

        return self.cleaned_data


class ProfileForm(BaseModelForm):
    """
    Form for the user profile page.
    """

    send_report = forms.BooleanField(
        label=_("Send daily report"),
        help_text=_("Check if you want to receive a daily report with information of all your checks"),
        required=False
    )

    def __init__(self, *args, **kwargs):
        """
        Fills the 'send_report' initial value.
        """

        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['send_report'].initial = self.get_extra().send_report

    def get_extra(self):
        """
        Returns (or creates) the UserExtra model related to the user.
        """

        try:
            extra = self.instance.userextra
        except:
            extra = models.UserExtra()
            extra.user = self.instance
            extra.send_report = True
            extra.save()

        return extra

    def save(self, *args, **kwargs):
        """
        Saves the user and the extra information.
        """

        extra = self.get_extra()
        extra.send_report = self.cleaned_data['send_report']
        extra.save()
        self.instance.save()

        return super(ProfileForm, self).save(*args, **kwargs)

    class Meta:
        model = User
        fields = ["username", "email", "send_report"]


class ChangePasswordForm(BaseForm):
    """
    Form for the password change process.
    """
    password = forms.CharField(label=_("New password"), widget=forms.PasswordInput)


#############################################################################

class CheckForm(BaseModelForm):
    class Meta:
        exclude = ['last_log_datetime', 'is_active', 'group']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4})
        }

class PingCheckForm(CheckForm):
    class Meta(CheckForm.Meta):
        model = models.PingCheck
        fields = ['target', 'title', 'description', 'check_interval', 'notify_email', 'should_check_timeout', 'timeout_value']

class DnsCheckForm(CheckForm):
    class Meta(CheckForm.Meta):
        model = models.DnsCheck
        fields = ['title', 'description', 'target', 'record_type', 'resolved_address', 'check_interval', 'notify_email']


class PortCheckForm(CheckForm):
    class Meta(CheckForm.Meta):
        model = models.PortCheck
        fields = ['title', 'description', 'target', 'target_port', 'response_check_string', 'check_interval', 'notify_email']


class HttpCheckForm(CheckForm):
    class Meta(CheckForm.Meta):
        model = models.HttpCheck
        fields = ['title', 'description', 'target', 'status_code', 'content_check_string', 'check_interval', 'notify_email']


