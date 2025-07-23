import json
from datetime import datetime

def createSales(request, cursor, mydb):
    body = json.loads(request.body.decode('utf-8'))
    sku_list = body.get('pid')                
    qty_dict = body.get('qty')                
    size = body.get('size')
    price = body.get('price')
    tax = body.get('tax')
    shipping = body.get('shipping')
    discount = body.get('discount')
    address = body.get('address')
    cName = body.get('cName')
    cMobile = body.get('cMobile')
    cUpazila = body.get('cUpazila')
    cDistrict = body.get('cDistrict')
    individualPrice_list = body.get('individualPrice')
    individualTax_list = body.get('individualTax') 
    indivualDiscount_list = body.get('indivualDiscount')
    created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    createCustomer(cursor,mydb,cName,cMobile,cUpazila,cDistrict,created_on)

    sid = findSalesId(cursor)
    print(body)
    qty_list = [str(qty_dict[sku]) for sku in sku_list]
    sku = ','.join(sku_list)
    qty = ','.join(qty_list)
    individualPrice = ','.join([str(i) for i in individualPrice_list])
    individualTax =  ','.join([str(i) for i in individualTax_list])
    indivualDiscount = ','.join([str(i) for i in indivualDiscount_list])

    query = """
        INSERT INTO sales (
            Sid, Cid, Pid, Qty, Size, Price,
            Tax, Shipping, Discount, Address,
            InvoiceDate,Status,PaidAmount,individualPrice,individualTax,individualDiscount
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending',%s, %s, %s, %s)
    """

    cursor.execute(query, [
        sid, cMobile[7:], sku, qty, size, price,
        tax, shipping, discount, address,
        created_on,0,individualPrice,individualTax,indivualDiscount
    ])
    mydb.commit()


def createCustomer(cursor,mydb,cName,cMobile,cUpazila,cDistrict,created_on):
    c="select Id from customer where Phone = '{}'".format(cMobile)
    cursor.execute(c)
    id = cursor.fetchone()

    if id is None:
        query = """
            INSERT INTO customer (Id, Name, Phone, Upazila, District, EntryTime)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (cMobile[7:], cName, cMobile, cUpazila, cDistrict, created_on))
        mydb.commit()
        return 1
    else:
        return 0

def findSalesId(cursor):
    cursor.execute("SELECT max(serial) FROM sales")
    result = cursor.fetchone()
    serial = result[0] if result else 0  
    current_year = datetime.now().year
    sid = "INV" + str(current_year) + str(serial + 1)
    return sid
