#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
import main_app

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

class LoginForm(BaseForm):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())

class AssessmentProcedureForm(BaseModelForm):
    class Meta:
        model = main_app.models.AssessmentProcedure
        exclude = ['tools']

class AssessmentToolForm(BaseModelForm):
    class Meta:
        model  = main_app.models.AssessmentTool