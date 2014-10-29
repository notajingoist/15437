from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
	return dictionary.get(key)

@register.filter(name='addcss')
def addcss(value, arg):
	return value.as_widget(attrs={'class': arg})

@register.filter(name='addplaceholder')
def addcss(value, arg):
	return value.as_widget(attrs={'placeholder': arg})