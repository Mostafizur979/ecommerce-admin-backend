import json
import base64
def updateSubCategory(request,cursor,mydb):
    body = json.loads(request.body)
    image_data = base64.b64decode(body.get("images").split(",")[-1]) if body.get("images") else None
    print("Title: ", body["title"])
    cursor.execute("""
        UPDATE product_sub_category SET
        categoryName=%s, currentStatus=%s, Image=%s
        WHERE categoryId=%s
        """, [
            body["title"], body["status"], image_data,body['id']
        ])
    mydb.commit()