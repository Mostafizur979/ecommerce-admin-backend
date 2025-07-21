import json
def createShippingAddress(request, cursor, mydb):
    body = json.loads(request.body.decode('utf-8'))
    name = body.get('name')   
    phone = body.get('phone')
    deliveryAddress = body.get('address')   
    division = body.get('division')
    district = body.get('district')
    upazila = body.get('upazila')
    provider = body.get('provider')
    query = """
            INSERT INTO shipping_address (customerPhone, customerName, deliveryAddress, division, district, upazila, shipmentprovider)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    cursor.execute(query, (phone,name,deliveryAddress,division,district,upazila,provider))
    mydb.commit()