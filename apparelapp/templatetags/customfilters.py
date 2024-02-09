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


# @register.filter(name='isbotwear')
# def isbotwear(value:str):
#     if value.strip() in ['Jeans','Trousers','Shorts','Underwears']:
#         return True
#     else:
#         return False
    
# @register.filter(name='istopwear')
# def istopwear(value:str):
#     if value.strip() in ['Shirts','Coats','Jackets']:
#         return True
#     else:
#         return False
    
# @register.filter(name='isfootwear')
# def isfootwear(value:str):
#     if value.strip() in ['Shoes']:
#         return True
#     else:
#         return False
