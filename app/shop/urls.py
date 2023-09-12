from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category_list_tree/', views.CategoryListTree.as_view()),
    path('category_list_tree/<int:pk>/', views.category_list_tree_detail),
    path('product_list/', views.product_list),
    path('product_list/<int:pk>/', views.product_list_detail),
    path('user/', views.User.as_view(), name='user'),
    path('bucket_post/', views.BucketPost.as_view(), name='bucket'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
