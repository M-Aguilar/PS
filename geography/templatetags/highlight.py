from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def highlight(value, search_term, autoescape=True):
    return mark_safe(replace_all(value, search_term))

#replaces words regardless of captalization
def replace_all(value, s_term):
	value = value.replace(s_term, "<span class='highlight'>%s</span>" % s_term)
	value = value.replace(s_term.lower(), "<span class='highlight'>%s</span>" % s_term.lower())
	value = value.replace(s_term.upper(), "<span class='highlight'>%s</span>" % s_term.upper())
	value = value.replace(s_term.capitalize(), "<span class='highlight'>%s</span>" % s_term.capitalize())
	return value