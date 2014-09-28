from django import template

register = template.Library()

@register.filter(name='addcss')
def addcss(value, arg):
	return value.as_widget(attrs={'class': arg})

@register.filter(name='addplaceholder')
def addcss(value, arg):
	return value.as_widget(attrs={'placeholder': arg})