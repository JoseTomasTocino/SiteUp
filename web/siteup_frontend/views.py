import logging
logger = logging.getLogger(__name__)

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic import View, TemplateView, RedirectView, CreateView, UpdateView
from django.views.generic.edit import FormView

from .forms import LoginForm, SignupForm, PingCheckForm, DnsCheckForm, HttpCheckForm, PortCheckForm
from siteup_api import models

# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm

    def form_valid(self, form):
        login(self.request, form.get_user())

        return redirect('dashboard')


def logout_view(request):
    logout(request)

    return redirect('home')


class SignupView(FormView):
    form_class = SignupForm
    template_name = "signup.html"

    def form_valid(self, form):
        user = User.objects.create_user(username=form.cleaned_data['username'],
                                        email=form.cleaned_data['email'],
                                        password=form.cleaned_data['password'])


        messages.info(self.request, _('User was created successfully. You can now login.'))
        return redirect('home')


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['check_groups'] = models.CheckGroup.objects.all()
        context['check_group_checks'] = {}

        for check_group in context['check_groups']:
            check_group.checks = []

            for check_type in models.CHECK_TYPES:
                check_group.checks.extend(check_type.objects.all())

        return context


class ProfileView(UpdateView):
    model = User
    template_name = "generic_form.html"
    fields = ['username', 'email', 'password']

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        context["form_title"] = _("Edit profile details")
        context["form_submit"] = _("Update details")

        return context

class GroupCreateView(CreateView):
    model = models.CheckGroup
    template_name = "generic_form.html"
    success_url = reverse_lazy("dashboard")
    fields = ['title']

    def form_valid(self, form):
        if form.is_valid():
          group = form.save(commit=False)
          group.owner = self.request.user
          group.save()
          messages.info(self.request, _("Group created successfully"))

        return super(GroupCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GroupCreateView, self).get_context_data(**kwargs)

        context["form_title"] = _("Create group of checks")
        context["form_submit"] = _("Create group")

        return context

class GroupUpdateView(UpdateView):
    model = models.CheckGroup
    template_name = "generic_form.html"
    success_url = reverse_lazy("dashboard")
    fields = ['title', 'is_active']

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data(**kwargs)

        context["form_title"] = _("Edit group")
        context["form_submit"] = _("Edit group")

        return context

###################################################################################

class ChooseCheckTypeTemplateView(TemplateView):
    template_name = 'checks/choose_check_type.html'

class CheckCreateBaseView(CreateView):
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.group = models.CheckGroup.objects.get(pk=self.kwargs['pk'])
            obj.save()

        return redirect('dashboard')


class PingCheckCreateView(CheckCreateBaseView):
    form_class = PingCheckForm
    model = models.PingCheck
    template_name = "generic_form.html"

    def get_context_data(self, **kwargs):
        context = super(PingCheckCreateView, self).get_context_data(**kwargs)

        context["form_title"] = _("Create new Ping check")
        context["form_submit"] = _("Create check")

        return context


class DnsCheckCreateView(CheckCreateBaseView):
    form_class = DnsCheckForm
    model = models.DnsCheck
    template_name = "generic_form.html"

    def get_context_data(self, **kwargs):
        context = super(DnsCheckCreateView, self).get_context_data(**kwargs)

        context["form_title"] = _("Create new Dns check")
        context["form_submit"] = _("Create check")

        return context


class PortCheckCreateView(CheckCreateBaseView):
    form_class = PortCheckForm
    model = models.PortCheck
    template_name = "generic_form.html"

    def get_context_data(self, **kwargs):
        context = super(PortCheckCreateView, self).get_context_data(**kwargs)

        context["form_title"] = _("Create new Port check")
        context["form_submit"] = _("Create check")

        return context


class HttpCheckCreateView(CheckCreateBaseView):
    form_class = HttpCheckForm
    model = models.HttpCheck
    template_name = "generic_form.html"

    def get_context_data(self, **kwargs):
        context = super(HttpCheckCreateView, self).get_context_data(**kwargs)

        context["form_title"] = _("Create new Http check")
        context["form_submit"] = _("Create check")

        return context