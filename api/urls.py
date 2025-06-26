from django.urls import path
from .views import category, products, subCategory

urlpatterns = [
    path('category/', category, name='category'),
    path('subcategory/', subCategory, name='subcategory'),
    path('products/',products, name='products')
]
