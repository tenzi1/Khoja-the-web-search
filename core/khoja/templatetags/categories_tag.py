
from django import template
from khoja.models import Category

register = template.Library()

@register.inclusion_tag("categories.html")
def get_category_list(current_category=None):
    return {'categories': Category.objects.all(),
            'act_cat': current_category }
