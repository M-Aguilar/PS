from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def cur_range(page_num,total):
	if total == 0:
		r = str(0)
	else:
		if page_num == 0:
			page_num = 1
		r = str(((int(page_num)-1)*10)+1)
	return r