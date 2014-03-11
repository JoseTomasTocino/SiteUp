import logging
logger = logging.getLogger(__name__)
oplogger = logging.getLogger("operations")

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render_to_response
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic import View, TemplateView, RedirectView, CreateView, UpdateView, DeleteView, RedirectView, DetailView
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


############################################################################
# USER MANAGEMENT


class LoginView(FormView):
    """
    View for the login page.

    On GET, it shows the form. On POST, tries to login the user.
    """
    template_name = "generic_form.html"
    form_class = LoginForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        oplogger.info(u"USER_LOGIN: User '{}' logged in ".format(form.get_user().username))

        if 'next' in self.request.GET:
            return redirect(self.request.GET.get('next'))
        else:
            return redirect('dashboard')

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)

        context["form_submit"] = _("Log in")
        context["form_class"] = "narrow"
        context["subactions"] = [ { 'url': 'password_reset', 'title': _("Forgot password?") } ]

        return context


class LogoutView(View):
    """
    View for the logout page.
    """
    def get(self, *args, **kwargs):
        oplogger.info(u"USER_LOGOUT: User '{}' logged out ".format(self.request.user.username))

        logout(self.request)

        return redirect('home')


class SignupView(FormView):
    """
    View for the signup process.
    """
    form_class = SignupForm
    template_name = "generic_form.html"

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )

        oplogger.info(u"USER_SIGNUP: User '{}' was created".format(user.username))

        messages.info(self.request, _('User was created successfully. You can now login.'))
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)

        context["form_submit"] = _("Sign up")
        context["form_class"] = "narrow"

        return context


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    View for the user profile panel.
    """
    model = User
    template_name = "generic_form.html"
    fields = ['username', 'email']
    success_url = reverse_lazy("dashboard")
    success_message = _("Your profile was changed successfully")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        oplogger.info(u"USER_UPDATE: User '{}' updated his profile".format(self.request.user.username))
        return super(ProfileView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        context["form_title"] = _("Edit profile details")
        context["form_submit"] = _("Update details")
        context["subactions"] = [ { 'url': 'changepassword', 'title': _("Change password") } ]

        return context


class ChangePasswordView(FormView):
    """
    View for the password change panel.
    """
    form_class = ChangePasswordForm
    template_name = "generic_form.html"
    success_message = _("Password changed correctly")

    def form_valid(self, form):
        oplogger.info(u"USER_PASS_CHANGE: User '{}' changed his password".format(self.request.user.username))

        self.request.user.set_password(form.cleaned_data['password'])
        self.request.user.save()
        messages.success(self.request, self.success_message)
        return redirect('dashboard')

    def get_context_data(self, **kwargs):
        context = super(ChangePasswordView, self).get_context_data(**kwargs)

        context["form_title"] = _("Change user password")
        context["form_submit"] = _("Change password")

        return context


def password_reset(request):
    context = {}
    context["form_submit"] = _("Send reset code")
    context["form_class"] = "narrow"
    context["site_name"] = "SiteUp"

    return auth_views.password_reset(
        request=request,
        template_name="generic_form.html",
        email_template_name="auth/password_reset_email.html",
        subject_template_name="auth/password_reset_subject.html",
        extra_context=context
    )

def password_reset_done(request):
    return auth_views.password_reset_done(
        request=request,
        template_name="auth/password_reset_done.html"
    )

def password_reset_confirm(request, uidb64, token):
    return auth_views.password_reset_confirm(
        request=request,
        uidb64=uidb64,
        token=token,
        template_name="generic_form.html",
        extra_context={
            'form_class': 'narrow',
            'form_submit': _('Set new password')
        }
    )

def password_reset_complete(request):
    return auth_views.password_reset_complete(
        request=request,
        template_name="auth/password_reset_complete.html"
    )



###################################################################################
# Dashboard


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['check_groups'] = self.request.user.checkgroup_set \
            .prefetch_related('dnscheck_set', 'pingcheck_set', 'httpcheck_set', 'portcheck_set', 'dnscheck_set__logs', 'pingcheck_set__logs', 'httpcheck_set__logs', 'portcheck_set__logs',)

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

          oplogger.info(u"GROUP_CREATE: User '{}' created group {},'{}'".format(self.request.user.username, group.pk, group.title))

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

    def form_valid(self, form):
        ret = super(GroupUpdateView, self).form_valid(form)
        oplogger.info(u"GROUP_UPDATE: User '{}' updated group {},'{}'".format(self.request.user.username, self.object.pk, self.object.title))
        return ret

    def get_queryset(self):
        qs = super(GroupUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data(**kwargs)

        context["form_title"] = _("Edit group")
        context["form_submit"] = _("Edit group")
        context["back_to"] = reverse_lazy("dashboard")

        return context


class GroupDeleteView(LoginRequiredMixin, DeleteMessageMixin, DeleteView):
    model = models.CheckGroup
    template_name = "generic_confirm.html"
    success_url = reverse_lazy("dashboard")
    deletion_message = _("Group deleted successfully")

    def delete(self, request, *args, **kwargs):
        oplogger.info(u"GROUP_DELETE: User '{}' deleted group {},'{}'".format(self.request.user.username, self.get_object().pk, self.get_object().title))
        return super(GroupDeleteView, self).delete(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(GroupDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(GroupDeleteView, self).get_context_data(**kwargs)
        context['back_to'] = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super(GroupDeleteView, self).get_context_data(**kwargs)
        context["back_to"] = reverse_lazy("dashboard")

        return context


class GroupEnableView(View):
    def get(self, request, *args, **kwargs):

        # Get the group
        group = models.CheckGroup.objects.get(pk=kwargs['pk'])

        # Check if the logged in user owns the group
        if group.owner != self.request.user:
            raise Http404

        # Enable the group
        group.enable()

        # Show success message
        messages.success(request, _("All checks within group were enabled"))

        oplogger.info(u"GROUP_ENABLE: User '{}' enabled group {},'{}'".format(self.request.user.username, group.pk, group.title))

        return redirect('dashboard')


class GroupDisableView(View):
    def get(self, request, *args, **kwargs):

        # Get the group
        group = models.CheckGroup.objects.get(pk=kwargs['pk'])

        # Check if the logged in user owns the group
        if group.owner != self.request.user:
            raise Http404

        # Disable teh group
        group.disable()

        # Show success message
        messages.success(request, _("All checks within group were disabled"))

        oplogger.info(u"GROUP_DISABLE: User '{}' disabled group {},'{}'".format(self.request.user.username, group.pk, group.title))

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

            oplogger.info(u"CHECK_CREATE: User '{}' created {} - id: {}, name: {}".format(self.request.user.username, obj.type_name(), obj.pk, obj.title))

        return redirect('dashboard')


class CheckUpdateView(GenericCheckViewMixin, LoginRequiredMixin, UpdateView):
    template_name = "generic_form.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        oplogger.info(u"CHECK_UPDATE: User '{}' updated {} - id: {}, name: {}".format(self.request.user.username, self.object.type_name(), self.object.pk, self.object.title))

        return super(CheckUpdateView, self).form_valid(form)

    def get_success_url(self):

        # Redirection depends on 'back_to' GET parameter (if it exists)

        back_to = self.request.GET.get('back_to', None)

        if back_to in (None, 'dashboard'):
            return reverse_lazy('dashboard')
        elif back_to == 'detail':
            return self.get_object().detail_url()

    def get_context_data(self, **kwargs):
        context = super(CheckUpdateView, self).get_context_data(**kwargs)

        verbose_name = self.get_model_class()._meta.verbose_name.capitalize()
        context["form_title"] = _("Update %(checktype)s") % { 'checktype': verbose_name }
        context["form_submit"] = _("Update check")
        context["back_to"] = self.get_success_url()

        return context


class CheckDeleteView(GenericCheckViewMixin, LoginRequiredMixin, DeleteMessageMixin, DeleteView):
    template_name = "generic_confirm.html"
    success_url = reverse_lazy("dashboard")
    deletion_message = _("Group deleted successfully")

    def delete(self, request, *args, **kwargs):

        # Get the object
        self.object = self.get_object()

        # Post to the logger
        oplogger.info(u"CHECK_DELETE: User '{}' deleted {} - id: {}, name: {}".format(self.request.user.username, self.object.type_name(), self.object.pk, self.object.title))

        # Call the original delete method
        return super(CheckDeleteView, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CheckDeleteView, self).get_context_data(**kwargs)

        # Url of the 'go back' button
        back_to = self.request.GET.get('back_to', None)

        if back_to in (None, 'dashboard'):
            context['back_to'] = reverse_lazy('dashboard')
        elif back_to == 'detail':
            context['back_to'] =  self.get_object().detail_url()

        return context

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


class CheckDetailView(GenericCheckViewMixin, LoginRequiredMixin, DetailView):
    template_name = "checks/detail.html"
    context_object_name = "check"
