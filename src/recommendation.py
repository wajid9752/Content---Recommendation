from django.db.models import Count
from .models import *


def recommendation_script(user):
    liked_categories = Category.objects.filter(
        category_contents__attributes__user=user,
        category_contents__attributes__is_like=True
    ).distinct()

    liked_categories_with_counts = liked_categories.annotate(
        num_likes=Count('category_contents__attributes', 
        filter=models.Q(category_contents__attributes__is_like=True))
    )
    
    sorted_categories = liked_categories_with_counts.order_by('-num_likes')

    
    most_liked_category = sorted_categories.first()
    second_most_liked_category = sorted_categories[1] if len(sorted_categories) > 1 else None
    

    data_list=[]
    if most_liked_category is not None:
        data_list.append(most_liked_category)
        if second_most_liked_category is not None:
            data_list.append(second_most_liked_category)
        
    return data_list




    
        


