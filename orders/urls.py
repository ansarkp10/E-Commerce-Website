from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('cart/', views.show_cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_item/<pk>/', views.remove_item_from_cart, name='remove_item'),
    path('payment/', views.payment_view, name='payment'),
    path('receipt/', views.bill_receipt, name='bill_receipt'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
