import logging
logger = logging.getLogger(__name__)
oplogger = logging.getLogger("operations")

from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

class CSRFExemptMixin(object):
    """
    Exempts a class-based view handling POSTed data from needing a CSRF token.
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)


class LoginView(CSRFExemptMixin, View):
    def post(self, request, *args, **kwargs):

        # Post request should have all the proper fields
        if set(request.POST.keys()) != set(('username', 'password', 'regid')):
            return HttpResponseBadRequest()

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        logger.info("Received login: %s - %s", username, password)

        # If the login is invalid or the user does not exist, return 403
        if user is None or not user.is_active:
            return HttpResponseForbidden()

        # Valid login. Save device's registration ID
        user.userextra.regid = request.POST['regid']
        user.userextra.save()

        return HttpResponse('{ "valid": 1 }')
