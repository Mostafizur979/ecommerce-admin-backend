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

            product_list.append(product)
        return  product_list

    except Exception as e:
        return e