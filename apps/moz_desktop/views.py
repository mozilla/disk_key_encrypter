# Create your views here.
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
import apps.site.models as site_models
import apps.site.forms as forms
from django.db.models import Q
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File
from django.db import connection
from settings import DBS_OPTIONS, PAGINATION_LENGTH
import mimetypes
import operator
import base64
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from apps.site.cef import log_cef
from django.conf import settings
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from functools import reduce


def user_has_claim(func):
    def wrap(request, *args, **kwargs):
        # This check is in addition to the check done by OpenResty and acts as
        # a redundant check for added security
        groups_header = request.META.get(settings.GROUPS_META_VAR, '')
        groups = groups_header.split('|') if groups_header else []
        found_allow_admin = False
        try:
            allow_admin = os.environ["ALLOW_ADMIN"]
            found_allow_admin = True
        except KeyError:
            allow_admin = False

        if not found_allow_admin:
            try:
                allow_admin = settings.ALLOW_ADMIN
            except AttributeError:
                allow_admin = False
        
        if not allow_admin or allow_admin == "False" or allow_admin == False:
            raise PermissionDenied
        if (hasattr(request, 'user') and request.user.is_authenticated and settings.OIDC_DESKTOP_CLAIM_GROUP is None):
            return func(request, *args, **kwargs)
        if (hasattr(request, 'user') and request.user.is_authenticated
                and settings.OIDC_DESKTOP_CLAIM_GROUP in groups ):
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    return wrap

@user_has_claim
def detail(request, id_value):
    error = None
    success = request.GET.get('success', False)
    disk = get_object_or_404(site_models.EncryptedDisk, id=id_value)
    if success:
        success = 'Successfully Uploaded'
    if request.method == "POST":
        form = forms.UploadFormDesktop(
                request.POST,
                request.FILES, instance=disk)
        try:
            if form.is_valid():
                f = form.save(commit=False)
                if request.POST.get('binary_blob-clear'):
                    f.binary_blob.delete()
                if form.cleaned_data['binary_blob']:
                    if isinstance(form.cleaned_data['binary_blob'], InMemoryUploadedFile):
                        t_file = form.cleaned_data['binary_blob']
                        t_file.seek(0)
                        f.file_data = t_file.read()
                if f.user:
                    f.email_address = f.user.username
                f.save()
                items = [
                    {'suser': request.user},
                    {'cs1Label': 'asset_tag'},
                    {'cs1': disk.asset_tag},
                    {'cs2Label': 'id'},
                    {'cs2': id_value},
                    {'duser': f.email_address}
                ]
                log_cef("AdminUpdate", "Desktop Admin Updated info for %s - %s" % (f.email_address, f.asset_tag), items)  # noqa
                success = 1
            return HttpResponseRedirect('?success=%s' % success)
        except ValueError:
            error = 'Validation Failed'
        except Exception as e:
            error = 'An unknown error has occurred %s' % e
    else:
        form = forms.UploadFormDesktop(instance=disk)
        items = [
            {'suser': request.user},
            {'cs1Label': 'asset_tag'},
            {'cs1': disk.asset_tag},
            {'cs2Label': 'id'},
            {'cs2': id_value},
            {'duser': disk.email_address}
        ]
        log_cef("AdminView", "Desktop Admin viewed info for %s - %s" % (disk.email_address, disk.asset_tag), items)  # noqa
    return render(request, 'detail.html', {
        'form': form,
        'id': id_value,
        'disk': disk,
        'success': success,
        'error': error,
        })


@user_has_claim
def upload(request):
    error = None
    success = request.GET.get('success', False)
    if success:
        success = 'Successfully Uploaded'
    if request.method == "POST":
        form = forms.UploadFormDesktopUpload(request.POST, request.FILES)
        try:
            if form.is_valid():
                f = form.save(commit=False)
                if request.POST.get('binary_blob-clear'):
                    f.binary_blob.delete()
                if f.user:
                    f.email_address = f.user.username
                f.save()
                items = [
                    {'user': request.user},
                    {'asset_tag': f.asset_tag},
                    {'duser': f.email_address}
                ]
                log_cef("AdminCreate", "Desktop Admin Created key for key for %s - %s" % (f.email_address, f.asset_tag), items)  # noqa
                return HttpResponseRedirect(reverse('desktop_admin'))
        except ValueError:
            error = 'Validation Failed'
        except Exception as e:
            error = 'An unknown error has occurred %s' % e
    else:
        form = forms.UploadFormDesktopUpload()
    return render(request, 'desktop_admin_upload.html', {
        'form': form,
        'id': id,
        'success': success,
        'error': error,
        })


@user_has_claim
def desktop_admin(request):
    l_list = site_models.EncryptedDisk.objects.order_by('id').all()
    paginator = Paginator(l_list, PAGINATION_LENGTH)
    page_number = request.GET.get('page', 1)
    try:
        l_list = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        l_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        l_list = paginator.page(paginator.num_pages)
    search_list = []
    search = ''
    if request.method == 'POST':
        search = request.POST['search']
        if search != '':
            filters = [
                          Q(**{"%s__icontains" % t: search})
                          for t in site_models.EncryptedDisk.search_fields
                      ]
            search_list = site_models.EncryptedDisk.objects.filter(
                    reduce(operator.or_, filters)
                    )

    return render(request, 'list.html', {
        'list': l_list,
        'search': search,
        'search_list': search_list,
        })


@user_has_claim
def download_attach(request, id):
    # Read file from database
    disk = get_object_or_404(site_models.EncryptedDisk, id=id)
    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'=' * (4 - missing_padding)
    decoded_data = str(base64.b64decode(data).decode("utf8"))
    """
    inMemFile = StringIO(disk.file_data)
    inMemFile.name = disk.file_name
    inMemFile.mode = 'rb'

    file_content = File(inMemFile)
    content_type, content_encoding = mimetypes.guess_type(disk.file_name)
    content_type = 'application/force-download'
    response = HttpResponse(
            content=file_content,
            content_type=content_type
            )
    response['Content-Disposition'] = 'attachment; filename=%s' % disk.file_name
    if content_encoding:
        response['Content-Encoding'] = content_encoding
    return response