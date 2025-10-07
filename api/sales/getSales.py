def getSales(cursor):
    c="select * from sales order by InvoiceDate desc"
    cursor.execute(c)
    result = cursor.fetchall()

    dataList = []
    for x in result:
        data = {
            'sid' : x[0],
            'cid' : x[1],
            'pid' : x[2],
            'qty' : x[3],
            'size' : x[4],
            'subTotal' : x[5],
            'tax': x[6],
            'shipping': x[7],
            'discount': x[8],
            'deliveryAddress': x[9],
            'invoicedate' : x[10],
            'status' : x[15],
            'paid' : x[16]
        }
        dataList.append(data)
    print("data: ", dataList)
    return dataList