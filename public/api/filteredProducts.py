import base64
import json
def getFilteredProducts(cursor,request):
    try:
        categories = json.loads(request.GET.get("categories", "[]"))
        price_range = json.loads(request.GET.get("priceRange", '{"min":0,"max":999999}'))
        ascending = request.GET.get("ascending", "true") == "true"
        page = int(request.GET.get("page", 1))
        pageSize = int(request.GET.get("pageSize", 20))

        offset = (page - 1) * pageSize
        category_placeholders = ",".join(["%s"] * len(categories)) if categories else None

        if categories:
            if ascending:
                q = f"""
                    SELECT * FROM product 
                    WHERE Price >= %s AND Price <= %s 
                    AND Category IN ({category_placeholders}) 
                    ORDER BY Price ASC 
                    LIMIT %s OFFSET %s
                """
            else:
                q = f"""
                    SELECT * FROM product 
                    WHERE Price >= %s AND Price <= %s 
                    AND Category IN ({category_placeholders}) 
                    ORDER BY Price DESC 
                    LIMIT %s OFFSET %s
                """
            params = [price_range['min'], price_range['max']] + categories + [pageSize, offset]

            c = f"""
                SELECT COUNT(SKU) FROM product 
                WHERE Price >= %s AND Price <= %s 
                AND Category IN ({category_placeholders})
            """
            count_params = [price_range['min'], price_range['max']] + categories
        else:
            if ascending:
                q = """
                    SELECT * FROM product 
                    WHERE Price >= %s AND Price <= %s 
                    ORDER BY Price ASC 
                    LIMIT %s OFFSET %s
                """
            else:
                q = """
                    SELECT * FROM product 
                    WHERE Price >= %s AND Price <= %s 
                    ORDER BY Price DESC 
                    LIMIT %s OFFSET %s
                """
            params = [price_range['min'], price_range['max'], pageSize, offset]

            c = "SELECT COUNT(SKU) FROM product WHERE Price >= %s AND Price <= %s"
            count_params = [price_range['min'], price_range['max']]


        cursor.execute(q, params)
        result = cursor.fetchall()

        cursor.execute(c, count_params)
        totalCount = cursor.fetchone()
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
            product_list.append(product)
        
        data = dict()
        data['totalCount'] = totalCount[0]
        data['page'] = page
        data['pageSize'] = pageSize
        data['productList'] = product_list
        return  data

    except Exception as e:
        return e
    
