from django.contrib.auth.middleware import RemoteUserMiddleware
from django.conf import settings

class CustomRemoteUserMiddleware(RemoteUserMiddleware):
    """
    Middleware for utilizing Web-server-provided authentication.

    This overrides the default META variable configured in RemoteUserMiddleware
    which is used to fetch the username from and instead uses the META variable
    defined in the REMOTE_USER_META_VAR setting
    """
    header=getattr(
        settings, 'REMOTE_USER_META_VAR', RemoteUserMiddleware.header)
