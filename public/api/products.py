import base64
def getProducts(cursor):
    try:
        cursor.execute('SELECT * FROM product')
        result = cursor.fetchall()
        product_list = []

        for x in result:
            product = {
                'id': x[0],
                'name': x[1],
                'categoryId': x[2],
                'subCategoryId': x[3],
                'unit': x[4],
                'qty': x[5],
                'price': x[6],
                'discount': x[8]
            }

            try:
               product['image'] = base64.b64encode(x[10]).decode('utf-8')
            except:
                product['image'] = "no-image"  
                
            product['descriptions'] = getProductDescription(product['id'],cursor)
            product['assets'] = getProductAssets(product['id'],cursor)
            product_list.append(product)
        return  product_list

    except Exception as e:
        return e
    
def getProductDescription(sku,cursor):
    q = "select * from product_description where productId='{}'".format(sku)    
    cursor.execute(q)
    result=cursor.fetchall()
            
    descriptionList = []
    for data in result:
        description = {
            'id' : data[1],
            'title': data[2],
            'description': data[3]
        }
        descriptionList.append(description)
    
    return descriptionList

def getProductAssets(sku,cursor):
    q= "select * from product_asset where productId = '{}'".format(sku)
    cursor.execute(q)
    result=cursor.fetchall()

    assetList = []
    for data in result:
        try:
            image = base64.b64encode(data[2]).decode('utf-8')
        except:
            image = "no-image" 
        asset = {
            'id': data[1],
            'image_url': image
        }
        assetList.append(asset)
    return assetList
    

