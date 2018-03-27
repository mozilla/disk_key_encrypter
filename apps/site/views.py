# top-level views for the project, which don't belong in any specific app

from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
import models
import forms
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import requires_csrf_token
from apps.site.cef import log_cef


class HomePage(TemplateView):
    template_name = "index.html"

@requires_csrf_token
def login_view(request):
    logout(request)
    username = ""
    password = ""
    error = None
    initial = {
            'username': username,
            'password': password
            }
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username = form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
            if user is not None:
                items = []
                items.append({'suser': username})
                items.append({'cs1Label': 'LoginSuccess'})
                items.append({'cs1': 'True'})
                log_cef("LoginSuccess", "Login Succeeded For %s" % user.email, items)
                if hasattr(user, 'is_desktop') and user.is_desktop:
                    """
                        Per bug #822396
                        Redirecting all logins to reverse('upload')
                        I can't replicate in dev, so going to test
                        to see if the issue is based on something
                        specific to an ldap bit for the user
                    """
                    return HttpResponseRedirect(reverse('upload'))
                    #return HttpResponseRedirect(reverse('desktop_admin'))
                else:
                    return HttpResponseRedirect(reverse('upload'))
            else:
                items = []
                items.append({'suser': username})
                items.append({'cs1Label': 'LoginSuccess'})
                items.append({'cs1': 'False'})
                log_cef("LoginFail", "Login Failed For %s" % username, items)
                error = 'Invalid Username/Password'
        else:
            error = 'Please supply both a username and password'
    else:
        form = forms.LoginForm(initial=initial)
    return render(request, 'login.html', {
        'username': username,
        'password': password,
        'form': form,
        'error': error,
        })

