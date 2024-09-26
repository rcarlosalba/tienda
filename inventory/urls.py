from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/',
         views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/',
         views.category_detail, name='category_detail'),
    path('category/<int:category_id>/',
         views.category_products, name='category_products'),
]
