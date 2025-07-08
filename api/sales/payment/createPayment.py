import json
from datetime import datetime

def createSalesPayment(request,cursor,mydb):
    body = json.loads(request.body.decode('utf-8'))
    sid = body.get('sid')
    method = body.get('method')
    amount =  body.get('amount')
    addedBy = body.get('addedBy')
    paymentDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pid = generatePaymentId(cursor)
    addPaymentIntoSales(sid,amount,cursor,mydb)
    c=""" 
       insert into payment (Id,Sid,PaymentMethod,Amount,AddedBy,PaymentDate) 
         values (%s,%s,%s,%s,%s,%s)
    """
    print(method)
    cursor.execute(c,[pid,sid,method,amount,addedBy,paymentDate])
    mydb.commit()


def generatePaymentId(cursor):
    c="select count(Id) from payment"
    cursor.execute(c)
    result = cursor.fetchone()
    count = result[0] if result else 0  
    print(count)
    current_year = datetime.now().year
    pid = "TRX-" + str(current_year) + str(count + 1)
    return pid

def addPaymentIntoSales(sid,amount,cursor,mydb):
    c="select PaidAmount from sales where Sid = '{}'".format(sid)
    cursor.execute(c)
    paid = cursor.fetchone()
    paidAmount = paid[0] if paid else 0  

    paidAmount = float(paidAmount) + float(amount)
    print(paidAmount)
    print(sid)
    c="update sales set PaidAmount = '{}' where Sid='{}'".format(paidAmount,sid)
    cursor.execute(c)
    mydb.commit()
   


