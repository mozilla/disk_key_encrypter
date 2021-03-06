"""
WSGI config for desktop_signing_webapp project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.

application = get_wsgi_application()

# OpenIDC connection might require a proxy
try:
    from settings import USE_WSGI_OUTBOUND_PROXY
except:
    USE_WSGI_OUTBOUND_PROXY = False

try:
    from settings import WSGI_OUTBOUND_PROXY
except:
    WSGI_OUTBOUND_PROXY = ''

if USE_WSGI_OUTBOUND_PROXY is True:
    os.environ['http_proxy'] = WSGI_OUTBOUND_PROXY
    os.environ['https_proxy'] = WSGI_OUTBOUND_PROXY
