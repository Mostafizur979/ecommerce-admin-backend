from django.urls import path
from .views import products, categories,singleProduct, filteredProducts

urlpatterns = [
    path('products/', products, name='products'),
    path('categories/', categories, name='categories'),
    path('product/<str:id>/', singleProduct, name='product'),
    path('filtered-product/', filteredProducts, name='filteredProducts'),

]