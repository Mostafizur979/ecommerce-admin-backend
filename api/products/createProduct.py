import json
import base64
from datetime import datetime

def createProduct(request, cursor, mydb):
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
    image_data = body.get('images')
    description = body.get('description')
    title = body.get('descTitle')
    created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if len(image_data) > 0:
        image_binary = base64.b64decode(image_data[0].split(',')[-1])
    else:
        image_binary = None

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
        image_binary, "none", created_on
    ])
    mydb.commit()

    id = 0
    for data in description:
        id = id + 1
        query = """INSERT INTO product_description ( 
           productId, descriptionId, title, description 
        ) VALUES (%s,%s,%s,%s)
        """
        cursor.execute(query, [sku,id,data['title'], data['description']])
        mydb.commit()
    
    id = 0
    for data in image_data:
        id = id + 1
        image_binary = base64.b64decode(data.split(',')[-1])
        query = """ INSERT INTO product_asset (
          productId, assetId, assetUrl
        ) VALUES(%s,%s,%s)
        """
        cursor.execute(query, [sku,id,image_binary])
        mydb.commit()


    
