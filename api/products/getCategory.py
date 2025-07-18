import base64
def getCategory(cursor):
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
            'count': categoryCount,
            'Image': ''
        }
        try:
            category['Image'] =  base64.b64encode(x[5]).decode('utf-8')
        except:
            category['Image'] =  "no-image"  
        dataList.append(category)
    return dataList