from django.urls import path
from .views import category, products

urlpatterns = [
    path('category/', category, name='category'),
    path('products/',products, name='products')
]
