import json
import base64

def updateProduct(request, cursor, mydb):
    body = json.loads(request.body)

    image_data = (
        base64.b64decode(body.get("images").split(",")[-1])
        if body.get("images")
        else None
    )

    cursor.execute(
        """
        UPDATE product SET
            Pname = %s,
            Category = %s,
            SubCategory = %s,
            Unit = %s,
            Qty = %s,
            Price = %s,
            DiscountType = %s,
            DiscountValue = %s,
            QtyAlert = %s,
            Image = %s,
            Description = %s
        WHERE SKU = %s
        """,
        [
            body["pname"],
            body["category"],
            body["subcategory"],
            body["unit"],
            body["qty"],
            body["price"],
            body["discountType"],
            body["discountValue"],
            body["qtyAlert"],
            image_data,
            body["description"],
            body["sku"]
        ]
    )

    mydb.commit()
