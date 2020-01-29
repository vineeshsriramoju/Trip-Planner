from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import AccountBalance, Statement, Pending_redeem,Pending_transactions
from django.core.mail import send_mail
from random import *
import uuid
from twilio.rest import Client
from datetime import datetime
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.db import connection,transaction
try:
    import httplib

except:
    import http.client as httplib

cost = None
book_date = None

def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False
@login_required(login_url='login')
def index(request):
    global cost
    global book_date
    cost = (request.GET.get('total_cost'))
    
    book_date = request.GET.get('book_date')
    balances = AccountBalance.objects.filter(user=request.user)
    print('\n\n\n\n')
    print('balance type',type(balances))
    print('\n\n\n')
    print(balances)
    balance = {'bal': balances,'cost':cost}
    return render(request, 'credits/index.html', context=balance)

@login_required(login_url='login')

def statement(request):
    transaction = Statement.objects.filter(user=request.user).order_by('-date')[:5]
    # cursor = connection.cursor()
    # cursor.execute('Select * from credits_statement where user = %s order by date limit 5;',(request.user))
    # transaction.commit()

    #print(transaction2)
    transaction_disp = {'trans': transaction}
    return render(request, 'credits/statement.html', context=transaction_disp)

def contact(request):
    return render(request, 'credits/contact.html')

def pending_redeem(request):
    redeem_amount = request.POST['redeem_amount']
    seed()
    code = get_random_string(length=6, allowed_chars='1234567890')

    if have_internet():
        temp = AccountBalance.objects.get(user=request.user)
        y1 = float(temp.balance) - float(redeem_amount)
        if float(redeem_amount) < 0:
            return HttpResponse('<html><script>alert("Enter valid amount");window.location="/credits";</script></html>')
        if y1 < 0:
            return HttpResponse('<html><script>alert("Insufficient Funds");window.location="/credits";</script></html>')
        else:
            send_mail(
                'Code for transaction',
                str(code),
                'itwsproject@gmail.com',
                ['santosh.265559@gmail.com'],
            )
            mobile_number = 9121467576

            auth_token = "7f7afc0c7b5a8e3b39b82d374af486a4"
            account_sid = "ACe24048a852b18d18ac49658450803864"
            try:
                client = Client(account_sid, auth_token)
                client.messages.create(
                    to="+91" + str(mobile_number),
                    from_="+18649900776",
                    body="Use {} code for verification.Amount requested to redeem is {}".format(code, redeem_amount))
            except:
                client = Client(account_sid, auth_token)
                client.messages.create(
                    to="+917842149220",
                    from_="+18649900776",
                    body="Use {} code for verification.Amount requested to redeem is {}".format(code, redeem_amount))

            #Pending_redeem.objects.create(user=request.user, redeem_amount=redeem_amount,transaction_id="RED"+uuid.uuid4().hex[:9].upper(), code=int(code))
            time = datetime.now()
            cursor = connection.cursor()
            cursor.execute('INSERT INTO credits_pending_redeem(transaction_date,code,transaction_id,user,redeem_amount) VALUES(%s,%s,%s,%s,%s);',(time, int(code), "RED" + uuid.uuid4().hex[:9].upper(), request.user, redeem_amount))
            transaction.commit()
            #Pending_redeem.objects.raw('INSERT INTO credits_pending_redeem(code,transaction_id,user,redeem_amount) VALUES(%d,%s,%s,%s);',(int(code),"RED"+uuid.uuid4().hex[:9].upper(),request.user,redeem_amount))
    else:
        return HttpResponse("Internet not available.Please check your connection" + '<html><head><script>history.pushState(null, null, location.href);window.onpopstate = function () {history.go(1);};</script><a href="/credits">Click here to go to home page</a></head></html>')
    return render(request, 'credits/pending_redeem.html')



def verify_sms(request):
    global cost
    global book_date
    code = int(request.POST['code'])
    temp1 = Pending_redeem.objects.get(code=code)
    print('\n\n\n')
    #print(temp1.query)
    # cursor = connection.cursor()
    # cursor.execute('Select * from credits_pending_redeem where code = %s',(code))
    # transaction.commit()
    redeem_amount = temp1.redeem_amount
    temp = AccountBalance.objects.get(user=request.user)
    y1 = float(temp.balance) - float(redeem_amount)
    key_err_page = "You have entered incorrect key" + '<html><head><script>history.pushState(null, null, location.href);window.onpopstate = function () {history.go(1);};</script><a href="/credits">Click here to go to home page</a></head></html>'
    key_success_page = "You have successfully redeemed {} credits from your account".format(redeem_amount) + '<html><head><script>history.pushState(null, null, location.href);window.onpopstate = function () {history.go(1);};</script><a href="/credits">Click here to go to home page</a></head></html>'
    if code == temp1.code:
            time = datetime.now()
            AccountBalance.objects.filter(user=request.user).update(balance=y1)
            #Statement.objects.create(user=request.user,amount=redeem_amount,transaction_id=temp1.transaction_id)
            #Statement.objects.raw('INSERT INTO "credits_statement"."user","credits_statement"."amount","credits_statement"."transaction_id") VALUES(?,?,?);',(request.user,redeem_amount,temp1.transaction_id))
            cursor = connection.cursor()
            cursor.execute('INSERT INTO credits_statement(date,user,amount,transaction_id) VALUES(%s,%s,%s,%s);',(time,request.user, redeem_amount, temp1.transaction_id))
            transaction.commit()
            temp1.delete()
            return HttpResponse(key_success_page)
    else:
        time = datetime.now()
        #Statement.objects.create(user=request.user, transaction_id="FAILED")
        #Statement.objects.raw('INSERT INTO credits_statement(user,transaction_id) VALUES(%s,%s);',(request.user ,"FAILED"))
        cursor = connection.cursor()
        cursor.execute('INSERT INTO credits_statement(date,user,amount,transaction_id) VALUES(%s,%s,%s,%s);',(time,request.user, redeem_amount, "FAILED"))
        transaction.commit()
        temp1.delete()
        return HttpResponse(key_err_page)


def random_key():
    seed()
    key = uuid.uuid4().hex[:8]
    return key

def redeem_cancel(request):
    time = datetime.now()
    temp = Pending_redeem.objects.get(user=request.user)
    #Statement.objects.create(user=request.user,transaction_id="CANCELLED")
    #Statement.objects.raw('INSERT INTO credits_statement(user,transaction_id) VALUES(%s,%s);', (request.user, "FAILED"))
    cursor = connection.cursor()
    cursor.execute('INSERT INTO credits_statement(date,user,transaction_id) VALUES(%s,%s,%s);',(time,request.user, "FAILED"))
    transaction.commit()
    temp.delete()
    return redirect('/credits')


def random_key():
    seed()
    key = uuid.uuid4().hex[:8]
    return key

def pending_transactions(request):
    add_amount = request.POST['add_amount']
    if float(add_amount) > 0:
        key = random_key()
        if have_internet():
            user_email = request.user.email
            Pending_transactions.objects.create(user=request.user, pending_amount=add_amount, key=key)
            subject = 'Payment confirmation'
            message = ('Please use this key for confirmation {}'.format(key))
            email_from = "santosh.265559@gmail.com"
            recipient_list = [user_email,]
            send_mail( subject, message, email_from, recipient_list)
            mobile_number = 9121467576

            auth_token = "7f7afc0c7b5a8e3b39b82d374af486a4"
            account_sid = "ACe24048a852b18d18ac49658450803864"
            try:
                client = Client(account_sid, auth_token)
                client.messages.create(
                    to="+91" + str(mobile_number),
                    from_="+18649900776",
                    body="Use {} code for verification.Amount requested to redeem is".format(key))
            except:
                pass
            return render(request, 'credits/pending_pay.html')
        else:
            return HttpResponse('<html><head><script>history.pushState(null, null, location.href);window.onpopstate = function () {history.go(1);};alert("Internet not available");window.location="/credits";</script></head></html>')

    else:
        return HttpResponse('<html><head><script>history.pushState(null, null, location.href);window.onpopstate = function () {history.go(1);};alert("Enter a valid amount");window.location="/credits";</script></head></html>')
def pending_transactions_paypal(request):
    add_amount = request.POST['add_amount']
    if float(add_amount) > 0:
        paypal = {'paypal':add_amount}
        if have_internet():
            Pending_transactions.objects.create(user=request.user, pending_amount=add_amount, key=random_key())
        else:
            return HttpResponse('<html><head><script>history.pushState(null, null, location.href);window.onpopstate = function () {history.go(1);};alert("Internet Not available");window.location="/credits";</script></head></html>')
        return render(request, 'credits/pending_pay_paypal.html', context=paypal)
    else:
        return HttpResponse('<html><head><script>history.pushState(null, null, location.href);window.onpopstate = function () {history.go(1);};alert("Enter a valid amount");window.location="/credits";</script></head></html>')

def confirm(request):
    pay_key = request.POST['pay_key']
    temp1 = Pending_transactions.objects.get(user=request.user)
    add_amount = temp1.pending_amount
    # temp2 = Statement.objects.get(user=1)
    # z1 = float(temp2.last1)
    # z2 = float(temp2.last2)
    # z3 = float(temp2.last3)
    # z4 = float(temp2.last4)
    # z5 = float(temp2.last5)
    key_err_page = '<html><head><script>history.pushState(null, null, location.href);window.onpopstate = function () {history.go(1);};alert("Key is incorrect");window.location="/credits";</script></head></html>'
    key_success_page = '<html><head><script>history.pushState(null, null, location.href);window.onpopstate = function () {history.go(1);};alert("Successfully added credits");window.location="/credits";</script></head></html>'
    if pay_key == temp1.key:
        temp = AccountBalance.objects.get(user=request.user)
        y1 = float(temp.balance) + float(add_amount)
        AccountBalance.objects.filter(user=request.user).update(balance=y1)

        Statement.objects.create(user=request.user,amount=add_amount,transaction_id=temp1.transaction_id)
        temp1.delete()
        return HttpResponse(key_success_page)
    else:

        Statement.objects.create(user=request.user,transaction_id="FAILED")
        temp1.delete()
        return HttpResponse(key_err_page)


def transaction_cancel(request):
    temp = Pending_transactions.objects.get(user=request.user)

    Statement.objects.create(user=request.user, transaction_id="CANCELLED")
    temp.delete()
    return redirect('/credits')


def paypal_confirm(request):
    val = request.POST['value']
    temp1 = Pending_transactions.objects.get(user=request.user)
    add_amount = temp1.pending_amount

    if val == "1":
        # p = Paypal_confirm.objects.get(user=1)
        # p.successful = 1
        # p.save()
        temp = AccountBalance.objects.get(user=request.user)
        y1 = float(temp.balance) + float(add_amount)
        AccountBalance.objects.filter(user=request.user).update(balance=y1)
        Statement.objects.create(user=request.user,transaction_id=temp1.transaction_id,amount=add_amount)
        temp1.delete()
    else:
        Statement.objects.create(user=request.user,transaction_id="CANCELLED")
        cursor = connection.cursor()
        cursor.execute('Insert into credits_statement(user,transaction_id,date) values(%s,%s,%s)',(request.user,"CANCELLED",datetime.now()))
        temp1.delete()
    return HttpResponse(status=200)
