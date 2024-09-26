from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),

    # Products
    path('products/', views.product_list, name='dashboard_product_list'),
    path('products/create/', views.product_create,
         name='dashboard_product_create'),
    path('products/<int:pk>/edit/', views.product_edit,
         name='dashboard_product_edit'),
    path('products/<int:pk>/delete/', views.product_delete,
         name='dashboard_product_delete'),
    path('delete-product-image/<int:image_id>/',
         views.delete_product_image, name='delete_product_image'),

    # Orders
    path('orders/', views.order_list, name='dashboard_order_list'),
    path('orders/<int:pk>/', views.order_detail, name='dashboard_order_detail'),

    # Categories
    path('categories/', views.category_list, name='dashboard_category_list'),
    path('categories/create/', views.category_create,
         name='dashboard_category_create'),
    path('categories/<int:pk>/edit/', views.category_edit,
         name='dashboard_category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete,
         name='dashboard_category_delete'),
]
