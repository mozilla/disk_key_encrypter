from django import template
from django.conf import settings

def has_admin_claim_group(request):
    r_context = {}
    r_context['has_admin_claim_group'] = False
    try:
        c_group = settings.OIDC_DESKTOP_CLAIM_GROUP
        if c_group in request.session['claim_groups']:
            r_context['has_admin_claim_group'] = True
    except:
        r_context['has_admin_claim_group'] = True
    return r_context
    
def allow_admin(request):
    r_context = {}
    try:
        r_context['allow_admin'] = settings.ALLOW_ADMIN
    except AttributeError:
        r_context['allow_admin'] = False
    return r_context
    
