from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import mysql.connector as sql
from .api.products import getProducts
from .api.categories import getCategory
from .api.singleProduct import getProduct
def database():
    mydb = sql.connect(
      host="localhost",
      user="root",
      password="",
      database="ecommerce_v2"
      )

    cursor=mydb.cursor()
    return cursor,mydb

@csrf_exempt
def products(request):
    cursor, mydb = database()    
    if request.method == 'GET':
        try:
            data = getProducts(cursor)
            return JsonResponse( data, safe=False)
        
        except Exception as e:
            return JsonResponse({'error': str(data)}, status=500)
        
@csrf_exempt
def categories(request):
    cursor, mydb = database()    
    if request.method == 'GET':
        try:
            data = getCategory(cursor)
            return JsonResponse( data, safe=False)
        
        except Exception as e:
            return JsonResponse({'error': str(data)}, status=500)
        
@csrf_exempt
def singleProduct(request, id):
    cursor, mydb = database()    
    if request.method == 'GET':
        try:
            data = getProduct(cursor,id)
            return JsonResponse( data, safe=False)
        
        except Exception as e:
            return JsonResponse({'error': str(data)}, status=500)