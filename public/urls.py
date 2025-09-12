from django.urls import path
from .views import products, categories

urlpatterns = [
    path('products/', products, name='products'),
    path('categories/', categories, name='categories'),
]