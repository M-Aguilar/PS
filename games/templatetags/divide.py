from django import template
register = template.Library()

@register.filter
def divide(value):
	if value['avg_rating']%1 == 0.0:
		return round(value['avg_rating'])
	else:
		return round(value['avg_rating'],1)

@register.filter
def full_path(value):
	return 'games/flag_svgs/{0}{1}'.format(value[-1], '.html')