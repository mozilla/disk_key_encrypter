#!/usr/bin/env python
import os
import sys
from django.core.management import call_command
from django.conf import settings

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            "desktop_signing_webapp.settings.testing"
            )
    applen = len('desktop_signing_webapp.apps.')
    apps_for_testing = [app[applen:] for app in settings.INSTALLED_APPS  # noqa
            if app.startswith("desktop_signing_webapp.apps")]

    call_command("test", *apps_for_testing)
