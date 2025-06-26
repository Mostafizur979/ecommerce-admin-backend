import json
from datetime import datetime
def createSubCategory(request,cursor,mydb):
    body = json.loads(request.body.decode('utf-8'))
    category = body.get('category')
    parentCategory = body.get('parentCategory')
    created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c="insert into product_sub_category (categoryName, createdOn, createdBy, currentStatus, parentCategory) values('{}','{}','{}','{}','{}')".format(category,created_on,"Mostafizur","Active",parentCategory)
    cursor.execute(c)
    mydb.commit()