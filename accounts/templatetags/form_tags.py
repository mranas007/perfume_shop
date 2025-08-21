from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    try:
        return value.as_widget(attrs={'class': arg})
    except Exception:
        # If value is not a BoundField (string or other), return as-is
        return value