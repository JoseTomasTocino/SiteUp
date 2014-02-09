from django.core.urlresolvers import reverse_lazy

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from django.db import IntegrityError

from django.shortcuts import redirect

from django.utils.translation import ugettext, ugettext_lazy as _

from django.views.generic import TemplateView, RedirectView, CreateView, UpdateView
from django.views.generic.edit import FormView

from .forms import LoginForm, SignupForm
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
            context['check_group_checks'][check_group.id] = []

            for check_type in models.CHECK_TYPES:
                context['check_group_checks'][check_group.id].extend(check_type.objects.all())

        return context


class ProfileView(TemplateView):
    pass

class GroupCreateView(CreateView):
    model = models.CheckGroup
    template_name = "generic_form.html"
    success_url = reverse_lazy("dashboard")
    fields = ['title']

    def get_initial(self):
        return { "owner": self.request.user }

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

