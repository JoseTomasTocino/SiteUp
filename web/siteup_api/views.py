import json, logging
logger = logging.getLogger("debugging")
oplogger = logging.getLogger("operations")

from django.contrib.auth import authenticate
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from django.core.urlresolvers import reverse

class CSRFExemptMixin(object):
    """
    Exempts a class-based view handling POSTed data from needing a CSRF token.
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)


class LoginView(CSRFExemptMixin, View):
    """
    View for the Android app, it logs in the user and returns his/her checks.
    """

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

        # Start building the response object
        response = {
            'valid': 1,
            'groups': []
        }

        # Go over user's CheckGroups
        for group in user.checkgroup_set.all():

            group_info = {
                'title': group.title,
                'checks': []
            }

            # Go over group's Checks
            for check in group.checks():

                group_info['checks'].append({
                    'title': check.title,
                    'description': check.description,
                    'status': 0 if check.last_status and check.last_status.status == 0 else 1,
                    'detail_url': ''.join([settings.BASE_URL, reverse("view_check", kwargs={'pk':check.pk, 'type':check.type_name()})]),
                })

            response['groups'].append(group_info)

        return HttpResponse(json.dumps(response))
