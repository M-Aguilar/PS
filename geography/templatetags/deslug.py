from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@stringfilter
@register.filter
def deslug(term):
	print(term)
	t = term
	if t == 'post_num':
		t = '# of posts'
	elif t == '-post_num':
		t = '-# of posts'
	elif 'date_edited' in t:
		t = t.replace('date_','')	
	elif 'date_added' in t:
		t = t.replace('date_added', 'created')
	if '_' in t:
		t = t.replace('_', ' ')
	return t
