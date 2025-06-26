import base64
def getSubCategory(cursor):
    c = "select * from product_sub_category"
    cursor.execute(c)
    result = cursor.fetchall()

    dataList = []
    for x in result:
        category = {
            'id': x[0],
            'name': x[1],
            'createdOn': x[2],
            'createdBy': x[3],
            'status': x[4],
            'Image': '',
            'parentCategory': x[6]
        }
        try:
            category['Image'] =  base64.b64encode(x[5]).decode('utf-8')
        except:
            category['Image'] =  "no-image"  
        dataList.append(category)
    return dataList