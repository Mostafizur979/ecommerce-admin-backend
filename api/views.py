from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import mysql.connector as sql
from django.db import connection
from datetime import datetime
import base64
import json
from .products.getProducts import getProducts
from .products.updateProduct import updateProduct
from .products.createProduct import createProduct   
from .products.getCategory import getCategory
from .products.updateCategory import updateCategory 
from .products.createCategory import createCategory   
from .products.createSubCategory import createSubCategory 
from .products.getSubCategory import getSubCategory
from .products.updateSubCategory import updateSubCategory
from .sales.createSales import createSales
from .sales.getSales import getSales
from .crm.customer.getCustomer import getCustomerInfo
from .sales.payment.createPayment import createSalesPayment
from .sales.payment.getPaymentList import getSalePayment
from .sales.createSales import createCustomer
from .shipping.createShipping import createShippingAddress
from .shipping.getShippingAddress import getShippingAddress
PRIVATE_KEY = "mysecretkey123"
def database():
    mydb = sql.connect(
      host="localhost",
      user="root",
      password="",
      database="nextadmin"
      )

    cursor=mydb.cursor()
    return cursor,mydb

@csrf_exempt
@require_http_methods(["POST","GET","PUT", "OPTIONS"])
def category(request):
    if request.method == "OPTIONS":
        return JsonResponse({}, status=200)
    client_key = request.headers.get('X-API-KEY')
    cursor, mydb = database()
    if request.method == 'POST':
        if client_key != PRIVATE_KEY:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        try:
            createCategory(request, cursor, mydb)
            return JsonResponse({'status': 'success', 'message': 'Category created successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        
    if request.method == 'GET':
        if client_key != PRIVATE_KEY:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        dataList = getCategory(cursor)
        return JsonResponse(dataList, safe=False)
    
    elif request.method == "PUT":
        try:
            updateCategory(request, cursor, mydb)
            return JsonResponse({"status": "success", "message": "Category updated"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST","GET","PUT", "OPTIONS"])
def subCategory(request):
    cursor, mydb = database()
    client_key = request.headers.get('X-API-KEY')
    if request.method == 'POST':
        if client_key != PRIVATE_KEY:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        try:
            createSubCategory(request, cursor, mydb)
            return JsonResponse({'status': 'success', 'message': 'Category created successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        
    elif request.method == 'GET':
        if client_key != PRIVATE_KEY:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        dataList = getSubCategory(cursor)
        return JsonResponse(dataList, safe=False)  
    elif request.method == "PUT":
        try:
            updateSubCategory(request, cursor, mydb)
            return JsonResponse({"status": "success", "message": "Category updated"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
 
@csrf_exempt
def products(request):
    cursor, mydb = database()
    if request.method == 'POST':
        try:
            createProduct(request, cursor, mydb)
            return JsonResponse({'status': 'success', 'message': 'Product created successfully'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        
    elif request.method == 'GET':
        try:
            data = getProducts(cursor)
            return JsonResponse( data, safe=False)
        
        except Exception as e:
            return JsonResponse({'error': str(data)}, status=500)
        
    elif request.method == "PUT":
        try:
            updateProduct(request, cursor, mydb)
            return JsonResponse({"status": "success", "message": "Product updated."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
        
    elif request.method == "DELETE":
        body = json.loads(request.body)
        try:    
            cursor.execute("DELETE FROM product WHERE SKU = %s", (body['sku']))
            mydb.commit()
            return JsonResponse({"status": "success", "message": "Product deleted."})
        except:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)    
        

@csrf_exempt
def sales(request):
    cursor, mydb = database()
    if request.method == 'POST':
        try:
            createSales(request, cursor, mydb)
            return JsonResponse({'status': 'success', 'message': 'successfully added sales'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    elif request.method == 'GET':
        try: 
            data = getSales(cursor)
            return JsonResponse(data, safe=False)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})    

@csrf_exempt        
def customer(request):
    cursor,mydb = database()
    if(request.method == 'GET'):
        try:
            data = getCustomerInfo(cursor)
            return JsonResponse( data, safe=False)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})    
    elif request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            cName = body.get('name')   
            mobile = body.get('mobile') 
            upazila = body.get('upazila')
            district = body.get('district')
            created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            status = createCustomer(cursor,mydb,cName,mobile,upazila,district,created_on)
            return JsonResponse({'status': 'success', 'message': status})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

                

@csrf_exempt
def salesPayment(request):
    cursor, mydb = database()
    if request.method == 'POST':
        try:
            createSalesPayment(request, cursor, mydb)
            return JsonResponse({'status': 'success', 'message': 'successfully added sales'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    elif request.method == 'GET':
        try: 
            data = getSalePayment(cursor)
            return JsonResponse(data, safe=False)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})  

@csrf_exempt
def shipping(request): 
    cursor, mydb = database()
    if request.method == 'POST':
        try:
            createShippingAddress(request, cursor, mydb)
            return JsonResponse({'status': 'success', 'message': 'successfully added shipping address'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}) 
        
    elif request.method == 'GET':
        try:
            phone = request.GET.get('phone')  
            provider = request.GET.get('provider')
            data = getShippingAddress(cursor, phone, provider)
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


