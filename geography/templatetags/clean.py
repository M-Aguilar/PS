from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@stringfilter
@register.filter
def clean(term):
	t = term
	t = t.replace('-','')
	t = t.replace('_', ' ')
	t = t.title()
	t = t.replace('Id', 'ID')
	t = t.replace('Num', '#')
	return t
