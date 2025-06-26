import json
from datetime import datetime
def createCategory(request,cursor,mydb):
    body = json.loads(request.body.decode('utf-8'))
    category = body.get('category')
    created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c="insert into product_category (categoryName, createdOn, createdBy, currentStatus) values('{}','{}','{}','{}')".format(category,created_on,"Mostafizur","Active")
    cursor.execute(c)
    mydb.commit()