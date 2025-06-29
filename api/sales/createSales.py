import json
import base64
from datetime import datetime

def createSales(request, cursor, mydb):
    body = json.loads(request.body.decode('utf-8'))
    print("body: "+body)
    sku = body.get('pid')
    qty = body.get('qty')
    size = body.get('size')
    price = body.get('price')
    tax = body.get('taxValue')
    shipping = body.get('shipping')
    discount = body.get('discount')
    address = body.get('address')
    cName = body.get('cName')
    cMobile = body.get('cMobile')
    cUpazila = body.get('cUpazila')
    cDistrict = body.get('cDistrict')
    created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    query = """
        INSERT INTO sales (
            Sid, Cid, Pid, Qty, Size, Price,
            Tax, Shipping, Discount, Address,
            InvoiceDate
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, [
        "1", "1", sku, qty, size, price,
        tax, shipping, discount, address,
        created_on
    ])
    mydb.commit()
