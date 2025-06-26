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
    created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if image_data:
        image_binary = base64.b64decode(image_data.split(',')[-1])
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
        image_binary, description, created_on
    ])
    mydb.commit()
