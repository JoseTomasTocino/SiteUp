import logging
logger = logging.getLogger("debugging")
oplogger = logging.getLogger("operations")

import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render_to_response
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic import View, TemplateView, RedirectView, CreateView, UpdateView, DeleteView, RedirectView, DetailView
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin

from bunch import Bunch

from .forms import LoginForm, SignupForm, ChangePasswordForm, PingCheckForm, DnsCheckForm, HttpCheckForm, PortCheckForm, ProfileForm
from siteup_api import models

############################################################################
# MY MIXINS


class DeleteMessageMixin(object):
    """
    Displays a flash message after an object has been deleted in a DeleteView.
    """

    deletion_message = None

    def delete(self, request, *args, **kwargs):

        # Delete the object
        self.object = self.get_object()
        self.object.delete()

        # If there's a deletion_message set, show it
        if self.deletion_message:
            messages.success(request, self.deletion_message)

        # Redirect to the success page
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
    View for the login page. On GET, it shows the form. On POST, tries to login the user.
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

        # Create the user
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )

        # Log the creation
        oplogger.info(u"USER_SIGNUP: User '{}' was created".format(user.username))

        # Create the extra info model
        models.UserExtra.objects.create(
            user=user,
            send_report=True
        )

        # Display the success message
        messages.info(self.request, _('User was created successfully. You can now login.'))

        # Redirect to the homepage
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
    # model = User
    # fields = ['username', 'email']
    form_class = ProfileForm

    template_name = "generic_form.html"
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

        # Fetch user's CheckGroups
        context['check_groups'] = self.request.user.checkgroup_set.all();

        # For each check group
        for check_group in context['check_groups']:
            check_group.template_data = Bunch()

            # Fetch group's checks
            check_group.template_data.checks = check_group.checks()

            # For each check
            for check in check_group.template_data.checks:

                check.template_data = Bunch()

                if check.last_status:
                    if check.last_status.status == 0:
                        check.template_data.status = 0
                    else:
                        check.template_data.status = 1
                else:
                    check.template_data.status = 0

                if not check.is_active:
                    check.template_data.active_class = 'inactive'

                # check.template_data.status = 0 if check.last_status and check.last_status.status == 0 else 1
                check.template_data.status_class = 'check-down' if check.template_data.status and check.template_data.status != 0 else ''
                # check.template_data.active_class = 'inactive' if not check.is_active else ''

        return context


@login_required
def get_dashboard_graph_data(request, check_type, check_id):

    if check_type == "httpcheck":
        check_class = models.HttpCheck
    elif check_type == "dnscheck":
        check_class = models.DnsCheck
    elif check_type == "portcheck":
        check_class = models.PortCheck
    else:
        check_class = models.PingCheck

    try:
        check = check_class.objects.get(id=check_id)
    except check_class.DoesNotExist:
        return HttpResponse('{}', content_type="application/json")

    if check.group.owner != request.user:
        raise Http404

    if check_type == "pingcheck":
        response_value = [(log.date.isoformat(), log.response_time) for log in check.logs.last_24_hours()]
    else:
        response_value = [(log.date.isoformat(), log.get_status()) for log in check.logs.last_24_hours()]

    return HttpResponse(json.dumps(response_value), content_type="application/json")


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
    """Simple view for the user to choose the kind of Check to create."""
    template_name = 'checks/choose_check_type.html'


class GenericCheckViewMixin(object):
    """
    Base for views that handle single checks.
    """

    def __init__(self, *args, **kwargs):

        # DB is only hit once when trying to fetch the model class
        self.model_class_cache = None

    def get_model_class(self):
        """
        Returns the model class according to the `type` parameter passed via URL
        """

        # Get the actual model class using the ContentType framework
        if not self.model_class_cache:
            self.model_class_cache = ContentType.objects.get(app_label="siteup_api", model=self.kwargs['type']).model_class()

        # Only allow working with check types
        if self.model_class_cache not in models.CHECK_TYPES:
            raise Http404

        return self.model_class_cache

    def get_queryset(self):
        """
        Limits the queryset to the elements owned by the logged user.
        """
        return self.get_model_class().objects.filter(group__owner=self.request.user)

    def get_form_class(self):
        """Returns the form associated to the check type"""
        return CHECK_FORMS[self.get_model_class()]


class CheckCreateView(GenericCheckViewMixin, LoginRequiredMixin, CreateView):
    """View to create a new check"""

    template_name = "generic_form.html"

    def get_context_data(self, **kwargs):
        """Adds the proper labels to the form for the selected check type"""

        context = super(CheckCreateView, self).get_context_data(**kwargs)
        verbose_name = self.get_model_class()._meta.verbose_name.capitalize()
        context["form_title"] = _("Create new %(checktype)s") % {'checktype': verbose_name}
        context["form_submit"] = _("Create check")

        return context

    def form_valid(self, form):
        if form.is_valid():
            # Before actually saving the check, link it to its group check
            obj = form.save(commit=False)
            obj.group = models.CheckGroup.objects.get(pk=self.kwargs['pk'])
            obj.save()

            oplogger.info(u"CHECK_CREATE: User '{}' created {} - id: {}, name: {}".format(self.request.user.username, obj.type_name(), obj.pk, obj.title))

        return redirect('dashboard')


class CheckUpdateView(GenericCheckViewMixin, LoginRequiredMixin, UpdateView):
    """View to update a new check."""

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
        context["form_title"] = _("Update %(checktype)s") % {'checktype': verbose_name}
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
            context['back_to'] = self.get_object().detail_url()

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

    def get_context_data(self, **kwargs):
        context = super(CheckDetailView, self).get_context_data(**kwargs)

        periods = [
            {
                'title': 'Last 24 hours',
                'code': 'last_24',
                'logs': self.object.logs.in_period(check_type=self.object.type_name, hours=24),
                'statuses': self.object.statuses.in_period(hours=24)
            },
            {
                'title': 'Last week',
                'code': 'last_week',
                'logs': self.object.logs.in_period(check_type=self.object.type_name, days=7),
                'statuses': self.object.statuses.in_period(days=7)
            },
            {
                'title': 'Last month',
                'code': 'last_month',
                'logs': self.object.logs.in_period(check_type=self.object.type_name, days=30),
                'statuses': self.object.statuses.in_period(days=30)
            },
        ]

        context['periods'] = periods

        return context


class CheckExportLogsView(GenericCheckViewMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        """
        Returns the check's CheckLogs within the selected time period.
        """

        # Get the check
        check = self.get_queryset().get(pk=kwargs['pk'])

        # Get the period from the URL's query
        period = request.GET.get('period', None)

        # Fetch the logs
        if period in ('last_24', None):
            logs = check.logs.in_period(check_type=check.type_name, hours=24)

        elif period == 'last_week':
            logs = check.logs.in_period(check_type=check.type_name, days=7)

        else:
            logs = check.logs.in_period(check_type=check.type_name, days=30)

        # Turn the logs into JSON
        data = json.dumps([{
            'date': o.date.isoformat(),
            'status': o.status,
            'status_extra': o.status_extra,
            'response_time': o.response_time} for o in logs['objs']
        ])

        return HttpResponse(data, content_type="application/json")


class CheckExportStatusesView(GenericCheckViewMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        """
        Returns the check's CheckStatuses within the selected time period.
        """

        # Get the check
        check = self.get_queryset().get(pk=kwargs['pk'])

        # Get the period from the URL's query
        period = request.GET.get('period', None)

        # Fetch the statuses
        if period in ('last_24', None):
            statuses = check.statuses.in_period(hours=24)

        elif period == 'last_week':
            statuses = check.statuses.in_period(days=7)

        else:
            statuses = check.statuses.in_period(days=30)

        # Turn the statuses into JSON
        data = json.dumps([{
            'date_start': o.get_date_start(),
            'date_end': o.get_date_end(),
            'status': o.status,
            'status_extra': o.status_extra} for o in statuses
        ])

        return HttpResponse(data, content_type="application/json")
