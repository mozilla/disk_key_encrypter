# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
import apps.site.models as site_models
import apps.site.forms as forms
from django.db.models import Q
from database_storage import DatabaseStorage
from settings import DBS_OPTIONS, PAGINATION_LENGTH
import mimetypes
import operator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def detail(request, id):                                                                                                                                                                   
    error = None
    success = request.GET.get('success', False)
    disk = get_object_or_404(site_models.EncryptedDisk, id=id)
    if success:
        success = 'Successfully Uploaded'
    if request.method == "POST":
        form = forms.UploadFormDesktop(request.POST, request.FILES, instance=disk)
        try:
            if form.is_valid():
                f = form.save(commit=False)
                if request.POST.get('binary_blob-clear'):
                    f.binary_blob.delete()
                if f.user:
                    f.email_address = f.user.username
                f.save()
                success = 1
            return HttpResponseRedirect('?success=%s' % success)
        except ValueError:
            error = 'Validation Failed'
        except Exception, e:
            error = 'An unknown error has occured %s' % e
    else:
        form = forms.UploadFormDesktop(instance=disk)
    return render_to_response('detail.html', {
        'form': form,
        'id': id,
        'success': success,
        'error': error,
        },
        RequestContext(request))

@user_passes_test(lambda u: u.is_staff, login_url='/login/')
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
                success = 1
        except ValueError:
            error = 'Validation Failed'
        except Exception, e:
            error = 'An unknown error has occured %s' % e
    else:
        form = forms.UploadFormDesktopUpload()
    return render_to_response('desktop_admin_upload.html', {
        'form': form,
        'id': id,
        'success': success,
        'error': error,
        },
        RequestContext(request))

@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def desktop_admin(request):                                                                                                                                                                   
    list = site_models.EncryptedDisk.objects.all()
    paginator = Paginator(list, PAGINATION_LENGTH)
    page_number = request.GET.get('page', 0)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list = paginator.page(paginator.num_pages)
    search_list = []
    search = ''
    if request.method == 'POST':
        search = request.POST['search']
        if search != '':
            filters = [Q(**{"%s__icontains" % t: search})
                        for t in site_models.EncryptedDisk.search_fields]
            search_list = site_models.EncryptedDisk.objects.filter(reduce(operator.or_, filters))

    return render_to_response('list.html', {
        'list': list,
        'search':search,
        'search_list': search_list,
        },
        RequestContext(request))

@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def download_attach(request, filename):
        # Read file from database
        storage = DatabaseStorage(DBS_OPTIONS)
        gpg_file = storage.open(filename, 'rb')
        if not gpg_file:
            raise Http404
        file_content = gpg_file.read()
       
        # Prepare response
        content_type, content_encoding = mimetypes.guess_type(filename)
        response = HttpResponse(content=file_content, mimetype=content_type)
        response['Content-Disposition'] = 'inline; filename=%s' % filename
        if content_encoding:
            response['Content-Encoding'] = content_encoding
        return response
