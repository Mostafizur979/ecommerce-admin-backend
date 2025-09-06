import base64
def getProducts(cursor):
    try:
        cursor.execute('SELECT * FROM product')
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

        product_list = []

        for row in rows:
            product = dict(zip(columns, row))
            try:
               product['Image'] = base64.b64encode(product['Image']).decode('utf-8')
            except:
                product['Image'] = "no-image"  
                
            product['descriptions'] = getProductDescription(product['SKU'],cursor)
            product['assets'] = getProductAssets(product['SKU'],cursor)
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
    