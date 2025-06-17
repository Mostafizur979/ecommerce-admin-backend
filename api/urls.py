from django.urls import path
from .views import get_category,receive_data, create_product, get_products

urlpatterns = [
    path('category/', get_category, name='get_data'),
    path('receive/', receive_data, name='receive_data'),
    path('createproduct/', create_product, name='createproduct'),
    path('getproducts/',get_products, name='get_products')
]
