# Create your views here.
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from apps.site import forms
from django.urls import reverse
from apps.site.cef import log_cef


def remote_user_login_required(func):
    # https://www.adelton.com/django/external-authentication-for-django-projects#idm139850931541280
    # https://code.djangoproject.com/ticket/25164
    def wrap(request, *args, **kwargs):
        if hasattr(request, 'user') and request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    return wrap

def index_upload(request):
    return HttpResponseRedirect(reverse("upload"))

@remote_user_login_required
def upload(request):
    error = None
    success = request.GET.get('success', False)
    items = [{'suser': request.user}]
    log_cef("UserUpload", "User uploaded new key", items)
    if success:
        success = 'Successfully Uploaded'
    if request.method == "POST":
        form = forms.UploadFormUser(request.POST, request.FILES)
        if form.is_valid():
            try:
                f = form.save(commit=False)
                f.user = request.user
                f.email_address = request.user.username
                if form.cleaned_data['binary_blob']:
                    f.file_data = form.cleaned_data['binary_blob']
                    f.file_name = form.files['binary_blob'].name
                f.save()
                success = 1
                items = [
                    {'user': request.user},
                    {'asset_tag': f.asset_tag}
                ]
                log_cef("UserUpload", "User uploaded new key", items)
                return HttpResponseRedirect('?success=%s' % success)
            except ValueError:
                error = 'Validation Failed'
            except Exception as e:
                error = 'An unknown error has occurred %s' % e
        else:
            form = forms.UploadFormUser()
            error = form.errors
    else:
        form = forms.UploadFormUser()
    return render(request, 'upload.html', {
        'form': form,
        'success': success,
        'error': error,
        })
