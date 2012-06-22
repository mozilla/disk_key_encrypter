# top-level views for the project, which don't belong in any specific app

from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
import models
import forms
from django.contrib.auth import login, logout, authenticate


class HomePage(TemplateView):
    template_name = "index.html"

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
            if user.is_active:
                login(request, user)
            if user is not None:
                if user.is_desktop:
                    return HttpResponseRedirect(reverse('desktop_admin'))
                else:
                    return HttpResponseRedirect(reverse('upload'))
            else:
                error = 'Invalid Username/Password'
        else:
            error = 'Please supply both a username and password'
    else:
        form = forms.LoginForm(initial=initial)
    return render_to_response('login.html', {
        'username': username,
        'password': password,
        'form': form,
        'error': error,
        },
        RequestContext(request))

