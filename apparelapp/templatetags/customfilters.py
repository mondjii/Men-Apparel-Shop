from django import template
register = template.Library()


@register.filter(name='add_id')
def add_id(value, arg) -> str:
    value.field.widget.attrs['id'] = arg
    return value


@register.filter(name='add_class')
def add_class(value,arg):
    value.field.widget.attrs['class'] = arg
    return value
