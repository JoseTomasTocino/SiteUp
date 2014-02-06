from django.views.generic import TemplateView, RedirectView
from django.views.generic.edit import FormView

from django.contrib.auth import authenticate, login, logout

from django.shortcuts import redirect

from .forms import LoginForm, SignupForm

# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('home')


class SignupView(FormView):
    form_class = SignupForm
    template_name = "signup.html"

