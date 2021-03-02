from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@stringfilter
@register.filter
def deslug(term):
	t = term
	if '-' in t:
		t = t.replace('-','')
	return t
