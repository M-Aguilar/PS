from django import template
register = template.Library()

@register.filter
def divide(value):
	if value['avg_rating']%1 == 0.0:
		return round(value['avg_rating'])
	else:
		return round(value['avg_rating'],1)
