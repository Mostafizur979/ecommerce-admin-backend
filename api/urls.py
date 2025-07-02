from django.urls import path
from .views import category, products, subCategory, sales, customer

urlpatterns = [
    path('category/', category, name='category'),
    path('subcategory/', subCategory, name='subcategory'),
    path('products/',products, name='products'),
    path('sales/',sales, name="sales"),
    path('customer/',customer,name="customer")
]
