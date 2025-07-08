def getSalePayment(cursor):
    c="select * from payment order by PaymentDate desc"
    cursor.execute(c)
    result = cursor.fetchall()

    dataList = []

    for x in result:
        data = {
            'id' : x[0],
            'sid' : x[1],
            'method': x[2],
            'amount': x[3],
            'author': x[4],
            'date': x[5]
        }
        dataList.append(data)
        
    return dataList