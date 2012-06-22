from django import template
register = template.Library()

@register.simple_tag
def active_page(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''
