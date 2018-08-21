from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.conf import settings


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def verify_claims(self, claims):
        super(CustomOIDCAuthenticationBackend, self).verify_claims(claims)
        try:
            claim_group_path = settings.OIDC_CLAIM_GROUPS_PATH
        except AttributeError:
            claim_group_path = None

        if claim_group_path:
            self.request.session['claim_groups'] = claims[claim_group_path]
        # claims don't need verified for access, just need to get them
        # to check for roles later
        return True
