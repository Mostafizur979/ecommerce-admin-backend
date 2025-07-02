def getCustomerInfo(cursor):
    c="select * from customer"
    cursor.execute(c)
    result = cursor.fetchall()
    dataList = []
    for x in result:
        data = {
            'id' : x[0],
            'name' : x[1],
            'phone' : x[2],
            'upazila': x[3],
            'district': x[4]
        }
        dataList.append(data)

    return dataList