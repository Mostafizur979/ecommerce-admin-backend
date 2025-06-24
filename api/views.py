from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import mysql.connector as sql
from django.db import connection
from datetime import datetime
import base64
import json
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
@require_http_methods(["GET","PUT", "OPTIONS"])
def get_category(request):
    if request.method == "OPTIONS":
        return JsonResponse({}, status=200)

    client_key = request.headers.get('X-API-KEY')
    if request.method == 'GET':
        if client_key != PRIVATE_KEY:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        
        cursor, mydb = database()
        c = "select * from product_category"
        cursor.execute(c)
        result = cursor.fetchall()

        dataList = []
        for x in result:
            c="select count(SKU) from product where Category='{}'".format(x[1])
            cursor.execute(c)
            categoryCount = cursor.fetchone()
            category = {
                'id': x[0],
                'name': x[1],
                'createdOn': x[2],
                'createdBy': x[3],
                'status': x[4],
                'count': categoryCount
            }
            dataList.append(category)
            
        return JsonResponse(dataList, safe=False)
    elif request.method == "PUT":
        try:
            body = json.loads(request.body)
            cursor, mydb = database()
            image_data = base64.b64decode(body.get("images").split(",")[-1]) if body.get("images") else None
            cursor.execute("""
                UPDATE product_category SET
                    categoryName=%s, currentStatus=%s, Image=%s
                    WHERE categoryName=%s
            """, [
                body["title"], body["status"], image_data,  body['title']
            ])
            mydb.commit()
            return JsonResponse({"status": "success", "message": "Category updated"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)



@csrf_exempt  # Disable CSRF for testing — only for development!
def receive_data(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            category = body.get('category')
            message = f"Hello, {category}! Data received successfully."
            created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor,mydb = database()
            c="insert into product_category (categoryName, createdOn, createdBy, currentStatus) values('{}','{}','{}','{}')".format(category,created_on,"Mostafizur","Active")
            cursor.execute(c)
            mydb.commit()
            return JsonResponse({'status': 'success', 'message': message})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            sku = body.get('sku')
            pname = body.get('pname')
            category = body.get('category')
            subcategory = body.get('subcategory')
            unit = body.get('unit')
            qty = body.get('qty')
            price = body.get('price')
            discountType = body.get('discountType')
            discountValue = body.get('discountValue')
            qtyAlert = body.get('qtyAlert')
            image_data = body.get('images')  # base64 string
            description = body.get('description')
            created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if image_data:
                image_binary = base64.b64decode(image_data.split(',')[-1])
            else:
                image_binary = None

            cursor, mydb = database()
            query = """
                INSERT INTO product (
                    SKU, Pname, Category, SubCategory, Unit, Qty,
                    Price, DiscountType, DiscountValue, QtyAlert,
                    Image, Description, CreatedOn
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, [
                sku, pname, category, subcategory, unit, qty,
                price, discountType, discountValue, qtyAlert,
                image_binary, description, created_on
            ])
            mydb.commit()

            return JsonResponse({'status': 'success', 'message': 'Product created successfully'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def get_products(request):
    cursor, mydb = database()
    if request.method == 'GET':
        try:
            cursor.execute('SELECT * FROM product')
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

            product_list = []

            for row in rows:
                product = dict(zip(columns, row))

                # Convert any bytes field to base64 string
                for key, value in product.items():
                    if isinstance(value, bytes):
                        product[key] = base64.b64encode(value).decode('utf-8')

                product_list.append(product)

            return JsonResponse( product_list, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    elif request.method == "PUT":
        try:
            body = json.loads(request.body)
            image_data = base64.b64decode(body.get("images").split(",")[-1]) if body.get("images") else None
            cursor.execute("""
                UPDATE product SET
                    Pname=%s, Category=%s, SubCategory=%s, Unit=%s, Qty=%s,
                    Price=%s, DiscountType=%s, DiscountValue=%s, QtyAlert=%s,
                    Image=%s, Description=%s
                WHERE SKU=%s
            """, [
                body["pname"], body["category"], body["subcategory"], body["unit"],
                body["qty"], body["price"], body["discountType"], body["discountValue"],
                body["qtyAlert"], image_data, body["description"], body['sku']
            ])
            mydb.commit()
            return JsonResponse({"status": "success", "message": "Product updated."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
        
    elif request.method == "DELETE":
        body = json.loads(request.body)
        try:    
            cursor.execute("DELETE FROM product WHERE SKU = %s", (body['sku'],))
            mydb.commit()
            return JsonResponse({"status": "success", "message": "Product deleted."})
        except:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)    