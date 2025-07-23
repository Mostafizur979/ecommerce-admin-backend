def getShippingAddress(cursor,phone,provider):
    c = "select * from shipping_address where customerPhone='{}' and shipmentprovider='{}'".format(phone,provider)
    cursor.execute(c)
    result = cursor.fetchall()
    data = []
    for x in result:
        address = {
            'cPhone': x[0],
            'cName': x[1],
            'address': x[2],
            'division': x[3],
            'district': x[4],
            'upazila': x[5],
            'provider': x[6]
        }
        data.append(address)
    return data
