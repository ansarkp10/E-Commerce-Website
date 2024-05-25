from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('product_list/', views.list_products, name='list_product'),
    path('product_detail/<int:pk>/', views.detail_product, name='detail_product'),
    path('search/', views.search_products, name='search_products'),  # Add this line for search functionality
    path('order_to_cart/', views.order_to_cart, name='order_to_cart'),
    path('accounts/login/', views.orderlogin, name='account_login'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
