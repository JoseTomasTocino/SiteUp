import logging
logger = logging.getLogger(__name__)

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render_to_response
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic import View, TemplateView, RedirectView, CreateView, UpdateView, DeleteView, RedirectView
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin

from .forms import LoginForm, SignupForm, ChangePasswordForm, PingCheckForm, DnsCheckForm, HttpCheckForm, PortCheckForm
from siteup_api import models

############################################################################
# MY MIXINS

class DeleteMessageMixin(object):
    deletion_message = None

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        if self.deletion_message:
            messages.success(request, self.deletion_message)
        return HttpResponseRedirect(self.get_success_url())

############################################################################

class HomeView(TemplateView):
    """
    View for the homepage
    """
    template_name = "home.html"


class LoginView(FormView):
    """
    View for the login page.

    On GET, it shows the form. On POST, tries to login the user.
    """
    template_name = "login.html"
    form_class = LoginForm

    def form_valid(self, form):
        login(self.request, form.get_user())

        return redirect('dashboard')


class LogoutView(View):
    """
    View for the logout page.
    """
    def get(self, *args, **kwargs):
        logout(self.request)

        return redirect('home')


class SignupView(FormView):
    """
    View for the signup process.
    """
    form_class = SignupForm
    template_name = "signup.html"

    def form_valid(self, form):
        user = User.objects.create_user(username=form.cleaned_data['username'],
                                        email=form.cleaned_data['email'],
                                        password=form.cleaned_data['password'])


        messages.info(self.request, _('User was created successfully. You can now login.'))
        return redirect('home')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "generic_form.html"
    fields = ['username', 'email']

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        context["form_title"] = _("Edit profile details")
        context["form_submit"] = _("Update details")
        context["subactions"] = [ { 'url': 'changepassword', 'title': _("Change password") } ]

        return context


class ChangePasswordView(SuccessMessageMixin, FormView):
    form_class = ChangePasswordForm
    template_name = "generic_form.html"
    success_message = _("Password changed correctly")

    def form_valid(self, form):
        self.request.user.change_password(form.cleaned_data['password'])
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super(ChangePasswordView, self).get_context_data(**kwargs)

        context["form_title"] = _("Change user password")
        context["form_submit"] = _("Change password")

        return context


###################################################################################
# Dashboard


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['check_groups'] = self.request.user.checkgroup_set.prefetch_related('dnscheck_set', 'pingcheck_set', 'httpcheck_set', 'portcheck_set')
        for check_group in context['check_groups']:
            check_group.checks = []
            check_group.checks.extend(check_group.dnscheck_set.all())
            check_group.checks.extend(check_group.pingcheck_set.all())
            check_group.checks.extend(check_group.httpcheck_set.all())
            check_group.checks.extend(check_group.portcheck_set.all())

        return context


###################################################################################
# GROUPS



class GroupCreateView(LoginRequiredMixin, CreateView):
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


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = models.CheckGroup
    template_name = "generic_form.html"
    success_url = reverse_lazy("dashboard")
    fields = ['title']

    def get_queryset(self):
        qs = super(GroupUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data(**kwargs)

        context["form_title"] = _("Edit group")
        context["form_submit"] = _("Edit group")

        return context


class GroupDeleteView(LoginRequiredMixin, DeleteMessageMixin, DeleteView):
    model = models.CheckGroup
    template_name = "generic_confirm.html"
    success_url = reverse_lazy("dashboard")
    deletion_message = _("Group deleted successfully")

    def get_queryset(self):
        qs = super(GroupDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class GroupEnableView(View):
    def get(self, request, *args, **kwargs):
        group = models.CheckGroup.objects.get(pk=kwargs['pk'])
        if group.owner != self.request.user:
            raise Http404
        group.enable()
        messages.success(request, _("All checks within group were enabled"))

        return redirect('dashboard')


class GroupDisableView(View):
    def get(self, request, *args, **kwargs):
        group = models.CheckGroup.objects.get(pk=kwargs['pk'])
        if group.owner != self.request.user:
            raise Http404
        group.disable()
        messages.success(request, _("All checks within group were disabled"))

        return redirect('dashboard')


###################################################################################
# CHECK CRUD

CHECK_FORMS = {}
CHECK_FORMS[models.PingCheck] = PingCheckForm
CHECK_FORMS[models.HttpCheck] = HttpCheckForm
CHECK_FORMS[models.DnsCheck] = DnsCheckForm
CHECK_FORMS[models.PortCheck] = PortCheckForm


class ChooseCheckTypeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'checks/choose_check_type.html'


class GenericCheckViewMixin(object):
    """Base for views that handle single checks."""

    def __init__(self, *args, **kwargs):
        self.model_class_cache = None

    def get_model_class(self):
        """Returns the model class according to the `type` parameter passed via URL"""
        # TODO limit models to check types

        if not self.model_class_cache:
            self.model_class_cache = ContentType.objects.get(app_label="siteup_api", model=self.kwargs['type']).model_class()

        return self.model_class_cache

    def get_queryset(self):
        return self.get_model_class().objects.filter(group__owner=self.request.user)

    def get_form_class(self):
        """Returns the form associated to the check type"""
        return CHECK_FORMS[self.get_model_class()]


class CheckCreateView(GenericCheckViewMixin, LoginRequiredMixin, CreateView):
    template_name = "generic_form.html"

    def get_context_data(self, **kwargs):
        context = super(CheckCreateView, self).get_context_data(**kwargs)
        verbose_name = self.get_model_class()._meta.verbose_name.capitalize()
        context["form_title"] = _("Create new %(checktype)s") % { 'checktype': verbose_name }
        context["form_submit"] = _("Create check")

        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.group = models.CheckGroup.objects.get(pk=self.kwargs['pk'])
            obj.save()

        return redirect('dashboard')


class CheckUpdateView(GenericCheckViewMixin, LoginRequiredMixin, UpdateView):
    template_name = "generic_form.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super(CheckUpdateView, self).get_context_data(**kwargs)
        verbose_name = self.get_model_class()._meta.verbose_name.capitalize()
        context["form_title"] = _("Update %(checktype)s") % { 'checktype': verbose_name }
        context["form_submit"] = _("Update check")

        return context


class CheckDeleteView(GenericCheckViewMixin, LoginRequiredMixin, DeleteMessageMixin, DeleteView):
    template_name = "generic_confirm.html"
    success_url = reverse_lazy("dashboard")
    deletion_message = _("Group deleted successfully")


class CheckEnableView(GenericCheckViewMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        check = self.get_queryset().get(pk=kwargs['pk'])
        check.is_active = True
        check.save()
        messages.success(request, _("Check was enabled successfully"))
        return redirect('dashboard')


class CheckDisableView(GenericCheckViewMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        check = self.get_queryset().get(pk=kwargs['pk'])
        check.is_active = False
        check.save()
        messages.success(request, _("Check was disabled successfully"))
        return redirect('dashboard')