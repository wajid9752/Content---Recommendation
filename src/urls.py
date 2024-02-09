from django.urls import path
from .views import *


urlpatterns=[
    path("" , home , name="home") , 
    path("filter-category/" , filter_category , name="filter_category") , 
    path("dislike_likes_view/" , dislike_likes_view , name="dislike_likes_view") , 

    path("login/" , user_login ,            name="login") , 
    path("register/" , user_registration ,  name="register") , 
    path("logout/" , user_logout ,          name="logout") , 
    path("profile/" , profile , name="profile"),
    path("update-profile/" , update_profile , name="update-profile"),

    # content RELATED VIEWS 
    path('my-content-list/', my_content_list, name='my-content-list'),
    path('content-add/', add_content, name='add_content'),
    path('content-update/<int:content_id>/', update_content, name='update_content'),
    path('content-detail/<int:content_id>/', content_detail, name='content_detail'),
    path('content-delete/<int:content_id>/', delete_content, name='delete_content'),

    # recommendation_view
    path("recommendation-view/" , recommendation_view , name="recommendation-view"),

]

