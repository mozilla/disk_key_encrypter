from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import LoginForm
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
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
                    )
            if user:
                login(request, user)
            if user is not None:
                items = [
                    {'suser': username},
                    {'cs1Label': 'LoginSuccess'},
                    {'cs1': 'True'}
                ]
                log_cef("LoginSuccess", "Login Succeeded For %s" % user.email, items)  # noqa
                if hasattr(user, 'is_desktop') and user.is_desktop:
                    """
                        Per bug #822396
                        Redirecting all logins to reverse('upload')
                        I can't replicate in dev, so going to test
                        to see if the issue is based on something
                        specific to an ldap bit for the user
                    """
                    return HttpResponseRedirect(reverse('upload'))
                else:
                    return HttpResponseRedirect(reverse('upload'))
            else:
                items = [
                    {'suser': username},
                    {'cs1Label': 'LoginSuccess'},
                    {'cs1': 'False'}
                ]
                log_cef("LoginFail", "Login Failed For %s" % username, items)
                error = 'Invalid Username/Password'
        else:
            error = 'Please supply both a username and password'
    else:
        form = LoginForm(initial=initial)
    return render(request, 'login.html', {
        'username': username,
        'password': password,
        'form': form,
        'error': error,
        })
