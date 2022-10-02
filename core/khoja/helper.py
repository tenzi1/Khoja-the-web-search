#Retrieves the categories based on user typed input
from .models import Category

def get_category_list(max_results=0, starts_with=''):
    category_list = []

    if starts_with:
        category_list = Category.objects.filter(name__istartswith=starts_with)
    
    if max_results > 0:
        if len(category_list) > max_results:
            category_list = category_list[:max_results]

    return category_list