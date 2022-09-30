from django import template
from khoja.models import Category

register = template.Library()

@register.inclusion_tag('khoja/cats.html')
def get_category_list():
    return {'cats': Category.objects.all()}