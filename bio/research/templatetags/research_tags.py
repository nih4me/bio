from django import template
from research.models import Author, Corporate

register = template.Library()

@register.filter
def author_full_name(id):
    full_name = ''
    try:
        author = Author.objects.get(pk=id)
        full_name = f'{author.first_name} {author.last_name}'
    except Exception as e:
        print(e)
        full_name = 'Undefined'
    return full_name

@register.filter
def corporate_name(id):
    name = ''
    try:
        author = Corporate.objects.get(pk=id)
        name = f'{author.name}'
    except Exception as e:
        print(e)
        name = 'Undefined'
    return name
