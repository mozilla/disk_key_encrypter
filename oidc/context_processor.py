from django.conf import settings


def has_admin_claim_group(request):
    r_context = {}
    r_context['has_admin_claim_group'] = False
    try:
        c_group = settings.OIDC_DESKTOP_CLAIM_GROUP

        # This check is in addition to the check done by openresty and acts as
        # a redundant check for added security
        groups = request.META.get(settings.GROUPS_META_VAR, '').split('|')
        if c_group in groups:
            r_context['has_admin_claim_group'] = True
    except:
        r_context['has_admin_claim_group'] = False
    return r_context


def allow_admin(request):
    r_context = {}
    try:
        r_context['allow_admin'] = settings.ALLOW_ADMIN
    except AttributeError:
        r_context['allow_admin'] = False
    return r_context
