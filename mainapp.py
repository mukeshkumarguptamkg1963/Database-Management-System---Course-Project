from flask import Flask,render_template,request,flash,redirect,url_for,session,request,logging
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from MySQLdb import connect
import random
import smtplib
import hashlib
import random,json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

lis=[]
pls1=[]
pls2=[]
#config SQL
app.config['MYSQL_HOST']='127.0.0.1'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='myflaskapp'
app.config['MYSQL_CURSORCLASS']='DictCursor'
app.config['MYSQL_PORT']=5000

app.secret_key='secret1234'

#init
mysql=MySQL(app)

p=[]

#-------------------------admin page
@app.route('/admin',methods=['GET','POST'])
def admin():
    task1=getOrder0status()
    task2=getOrder1status()
    task3=getOrderService()
    task4=getEmps()
    task5=getVehicles()
    task6=getsan()
    task7=getbul()
    if request.form:
        res=request.form
        if 'admin' in res:
            print("admin in")
            if ('addr3' in session.keys()) and session['addr3']==request.remote_addr:
                return(render_template('1.0_admin.html',task1=task1,task2=task2,task3=task3,task4=task4,task5=task5,task6=task6,task7=task7))
            if res['password']=="password" and res['admin']=="admin":
                print("saaaaaaahi")
                session['admin']=res['admin']
                session['addr3']=request.remote_addr
                print("ADMIN LOGGED IN")
                return(render_template('1.0_admin.html',task1=task1,task2=task2,task3=task3,task4=task4,task5=task5,task6=task6,task7=task7))
            else:
                print("gallllat")
                return redirect('/login/notfound')
        elif 'salary4' in res:
            add_employee(res)
        elif 'regno' in res:
            add_vehicle(res)
        elif 'itemname1' in res:
            add_sanitaryItem(res)
        elif 'itemname2' in res:
            add_building_material(res)
        elif 'itemid1' in res:
            editItem1(res)
        elif 'itemid01' in res:
            deleteItem1(res)
        elif 'itemid2' in res:
            editItem2(res)
        elif 'itemid02' in res:
            deleteItem2(res)
        elif 'orderid3' in res:
            print("yes")
            service_allotment(res)
        elif 'dname' in res:
            print("saahi hai bhai")
            add_sdealer(res)
        elif 'dname1' in res:
            print("saahi hai bhai")
            add_bdealer(res)
        elif 'curr1' in res:
            print(" curr1 hai ")
            updatecurr1(res)
        elif 'curr2' in res:
            print(" curr2 hai ")
            updatecurr2(res)
        return render_template('1.0_admin.html',task1=task1,task2=task2,task3=task3,task4=task4,task5=task5,task6=task6,task7=task7)
    else:
        if ('addr3' in session.keys()) and session['addr3']==request.remote_addr:
            return render_template("1.0_admin.html",task1=task1,task2=task2,task3=task3,task4=task4,task5=task5,task6=task6,task7=task7)
        else:
            return redirect('/login/notfound')

def updatecurr1(res):
    try:
        print("****************************")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        #i=random.randint(101,10001)
        print("hello---------------------------")
        d.execute("""update employee set curr_avail=1 where emp_id={} """.format(res['empid']))
        print("end")
        c.commit()
        c.close()
        return True
    except:
        return False

def updatecurr2(res):
    try:
        print("****************************")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        #i=random.randint(101,10001)
        print("hello---------------------------")
        d.execute("""update vehicle set curr_avail=1 where vehicle_id={} """.format(res['vid']))
        print("end")
        c.commit()
        c.close()
        return True
    except:
        return False

def getOrder0status():
    try:
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        #select * from orders where order_date between adddate(now(),-12) and now();
        d.execute("""select * from orders where order_status=0 and order_date between adddate(now(),-7) and now() """)
        results = d.fetchall()
        print("end")
        print(results)
        c.commit()
        c.close()
        return results
    except:
        return False

def getOrder1status():
    try:
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        #select * from orders where order_date between adddate(now(),-12) and now();
        d.execute("""select * from orders where order_status=1 and order_delivery_status=0 and order_date between adddate(now(),-7) and now() """)
        results = d.fetchall()
        print("end")
        print(results)
        c.commit()
        c.close()
        return results
    except:
        return False

def getOrderService():
    try:
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        #select * from orders where order_date between adddate(now(),-12) and now();
        d.execute("""select s.service_id,s.order_id,s.vendor_id,s.date_of_delivery,o.order_delivery_status from service as s,orders as o where o.order_status=1 and o.order_id=s.order_id and o.order_date between adddate(now(),-7) and now() """)
        results = d.fetchall()
        print("end")
        print(results)
        c.commit()
        c.close()
        return results
    except:
        return False

def getEmps():
    try:
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        #select * from orders where order_date between adddate(now(),-12) and now();
        d.execute("""select * from employee """)
        results = d.fetchall()
        print("end")
        print(results)
        c.commit()
        c.close()
        return results
    except:
        return False

def getVehicles():
    try:
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        #select * from orders where order_date between adddate(now(),-12) and now();
        d.execute("""select * from vehicle """)
        results = d.fetchall()
        print("end")
        print(results)
        c.commit()
        c.close()
        return results
    except:
        return False

def getsan():
    try:
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        #select * from orders where order_date between adddate(now(),-12) and now();
        d.execute("""select * from sanitary_item """)
        results = d.fetchall()
        print("end")
        print(results)
        c.commit()
        c.close()
        return results
    except:
        return False
def getbul():
    try:
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        #select * from orders where order_date between adddate(now(),-12) and now();
        d.execute("""select * from building_material """)
        results = d.fetchall()
        print("end")
        print(results)
        c.commit()
        c.close()
        return results
    except:
        return False

def service_allotment(res):
    try:
        print(res)
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        print(res)
        for keys in res:
            print(res[keys])
        print("grg")
        i=random.randint(1,10000)
        d.execute("""insert into service(service_id,order_id,vendor_id,date_of_delivery) values({},{},{},'{}')""".format(i,res['orderid3'],res['empid'],res['date']))
        c.commit()
        d.execute("""update employee set curr_avail={} where emp_id={} """.format(0,res['empid']))
        c.commit()
        d.execute("""update orders set order_delivery_status={} where order_id={} """.format(1,res['orderid3']))
        c.commit()

        print("saahi")
        for key in res:
            if res[key]=="on":
                d.execute("""select vehicle_id from vehicle where registration_no='{}' """.format(key))
                r=d.fetchall()
                print("-->  ",r[0][0])
                d.execute("""insert into vehicle_service(vehicle_id,service_id) values({},{})""".format(r[0][0],i))
                c.commit()
                d.execute("""update vehicle set curr_avail={} where vehicle_id={} """.format(0,r[0][0]))
                c.commit()
        print("end")
        #d.execute("""select c.email from customer as c,orders as o where order_id={} and o.customer_id=c.customer_id """.format(res['orderid3']))
        #r=d.fetchall()
        #print("  -->  ",r[0][0])

        #string="Details of delivery:-  Order_ID : " + str(res['orderid3']) + " ;; Service ID : " + str(i) + " ;; vendor_id : " + str(res['empid']) + " ;; Expected Date of Delivery : " + str(res['date'])
        #print(string)
        #mail2((string),str(r[0][0]))

        #print("end2")
        c.commit()
        c.close()
        return True
    except:
        return False


@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if ('addr3' in session.keys()) and session['addr3']==request.remote_addr:
        return(render_template('1.0_admin.html'))
    return render_template('1.0_admin_login.html',)

def add_employee(res):
    try:
        print(res)
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()

        i=random.randint(1,10000)

        d.execute("""insert into employee(emp_id,name,email,contact_no,address,salary,curr_avail,date_of_hiring) values({},'{}','{}','{}','{}',{},{},'{}')""".format(i,res['name'],res['email'],res['contact'],res['address'],res['salary4'],0,res['date']))

        print("end")
        c.commit()
        c.close()
        return True

    except:
        return False

def add_vehicle(res):
    try:
        print(res)
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        i=random.randint(5000,6000)
        d.execute("""insert into vehicle(vehicle_id,registration_no,numberPlateInfo,curr_avail) values({},'{}','{}',{})""".format(i,res['regno'],res['npi'],1))
        print("end")
        c.commit()
        c.close()
        return True
    except:
        return False

def add_sanitaryItem(res):
    try:
        print("****************************")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        i=random.randint(101,10001)
        print("hello---------------------------")
        d.execute("""insert into sanitary_item(item_id,item_name,cost,current_stock,threshold) values({},'{}',{},{},{})""".format(i,res['itemname1'],res['cost'],res['currentstock'],res['threshold']))
        print("end")
        c.commit()
        c.close()
        return True
    except:
        return False

def add_building_material(res):
    try:
        print("****************************")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        i=random.randint(101,10001)
        print("hello---------------------------")
        d.execute("""insert into building_material(item_id,item_name,cost,current_stock,threshold) values({},'{}',{},{},{})""".format(i,res['itemname2'],res['purchasecost'],res['currentstock'],res['threshold']))
        print("end")
        c.commit()
        c.close()
        return True
    except:
        return False

def editItem1(res):
    try:
        print("****************************")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        #i=random.randint(101,10001)
        print("hello---------------------------")
        d.execute("""update sanitary_item set current_stock={} where item_id={} """.format(res['currentstock1'],res['itemid1']))
        print("end")
        c.commit()
        c.close()
        return True
    except:
        return False

def deleteItem1(res):
    try:
        print("****************************")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        #i=random.randint(101,10001)
        print("hello---------------------------")
        d.execute("""delete from sanitary_item where item_id={} """.format(res['itemid01']))
        print("end")
        c.commit()
        c.close()
        return True
    except:
        return False

def editItem2(res):
    try:
        print("****************************")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        print res
        #i=random.randint(101,10001)
        print("hello---------------------------")
        d.execute("""update building_material set current_stock={} where item_id={} """.format(res['currentstock2'],res['itemid2']))
        print("end")
        c.commit()
        c.close()
        return True
    except:
        return False

def deleteItem2(res):
    try:
        print("****************************")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        #i=random.randint(101,10001)
        print("hello---------------------------")
        d.execute("""delete from building_material where item_id={} """.format(res['itemid02']))
        print("end")
        c.commit()
        c.close()
        return True
    except:
        return False

def add_sdealer(res):
    try:
        print("****************************")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        i=random.randint(101,10001)
        print("hello---------------------------")
        d.execute("""insert into sanitaryware_dealer(dealer_id,dealer_name,email,contact_no,address) values({},'{}','{}','{}','{}')""".format(i,res['dname'],res['email'],res['contact'],res['address']))
        print("end")
        c.commit()
        c.close()
        return True
    except:
        return False

def add_bdealer(res):
    try:
        print("****************************")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        i=random.randint(101,10001)
        print("hello---------------------------")
        d.execute("""insert into building_material_dealer(dealer_id,dealer_name,email,contact_no,address) values({},'{}','{}','{}','{}')""".format(i,res['dname1'],res['email'],res['contact'],res['address']))
        print("end")
        c.commit()
        c.close()
        return True
    except:
        return False



#--------------------end admin------------------------------------

@app.route('/signup/verify',methods=['GET','POST'])
def verify():
    try:
        if request.form:
            res=request.form

            l=res['email']
            if not l:
                return redirect('/login/notfound')
            pls1.append(res)
            i=random.randint(100000,999999)
            pls2.append(str(i))
            mail(('Enter it to complete the signup .The Verification code is ' + str(i)),l)
        return render_template('1.3_veripage.html',l=l,res=res)
    except:
        return redirect('/login/notfound')

def mail(msg,email):
    fromemail='divyanshuguptadg1997@gmail.com'
    password='divyazgupta!1!1'
    subject="Verification code"
    message=handleemail(msg,subject)
    ser=smtplib.SMTP('smtp.gmail.com',587)
    ser.ehlo()
    ser.starttls()
    ser.login(str(fromemail),str(password))
    ser.sendmail(str(fromemail),[str(fromemail),str(email)],message.as_string())
    ser.close()

def mail2(msg,email):
    fromemail='divyanshuguptadg1997@gmail.com'
    password='divyazgupta!1!1'
    subject="Delivary Details"
    message=handleemail(msg,subject)
    ser=smtplib.SMTP('smtp.gmail.com',587)
    ser.ehlo()
    ser.starttls()
    ser.login(str(fromemail),str(password))
    ser.sendmail(str(fromemail),[str(fromemail),str(email)],message.as_string())
    ser.close()

def handleemail(msg,subject):
    message=MIMEMultipart()
    message['Subject']=subject
    part1=MIMEText(str(msg),'plain')
    message.attach(part1)
    return message


#-------------------------------------------------

@app.route('/home',methods=['GET','POST'])
def index():
    try:
        res=request.form
        print(res)
        if 'logout' in res:
            session.pop("email",None)
            session.pop("addr",None)
            print("prev  ",p)
            p.pop()
            lis.pop()
            print("next  ",p)
            return render_template('1.1_Home.html')
        elif 'update' in res:
            print("updated")
            session.pop("email",None)
            session.pop("addr",None)
            p.pop()
            lis.pop()
            updatecust(res)
            return render_template('1.1_Home.html')
        elif 'adminlogout' in res:
            session.pop("admin",None)
            session.pop("addr3",None)
            return render_template('1.1_Home.html')
        elif 'signup' in res:
            print("root")
            calfunction(res)
            return render_template('1.1_Home.html')
        else:
            return render_template('1.1_Home.html')

    except:
        return render_template('1.1_Home.html')

def updatecust(res):
    try:
        print("****************************")
        print(res)
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        #i=random.randint(101,10001)
        print("hello---------------------------")
        d.execute("""update customer set name ='{}' where customer_id={} """.format(res['name'],res['custid']))
        c.commit()
        d.execute("""update customer set email ='{}' where customer_id={} """.format(res['email'],res['custid']))
        c.commit()
        d.execute("""update customer set password ='{}' where customer_id={}  """.format(res['password'],res['custid']))
        c.commit()
        d.execute("""update customer set contact_no ='{}' where customer_id={}  """.format(res['contact'],res['custid']))
        c.commit()
        d.execute("""update customer set occupation ='{}' where customer_id={} """.format(res['occ'],res['custid']))
        c.commit()
        d.execute("""update customer set address ='{}' where customer_id={} """.format(res['addr'],res['custid']))
        c.commit()

        print("end")

        c.close()
        return True
    except:
        return False



@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('1.7_about.html')

@app.route('/instruction')
def instr_page():
    return (render_template('1.2_instr.html'))

@app.route('/login',methods=['GET','POST'])
def login():
    if ('addr' in session.keys()) and session['addr']==request.remote_addr:
        return redirect("/login/profile")
    return(render_template('1.4_login.html'))

@app.route('/signup',methods=['GET','POST'])
def signup():
    if ('addr' in session.keys()) and session['addr']==request.remote_addr:
        return redirect("/login/profile")
    return(render_template('1.3_signup.html'))

def calfunction(res):
    try:
        print(res)
        print("ererere")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        print("345345")


        i=random.randint(1,100000)
        for key in res:
            print(key,"  ->  ",res[key])
        s=create_signature(res['password'])
        print s,"hashed password"
        d.execute("""insert into customer(customer_id,name,email,password,contact_no,occupation,address) values({},'{}','{}','{}','{}','{}','{}')""".format(i,res['name'],res['email'],s,res['contact'],res['occ'],res['addr']))

        print("end")
        c.commit()
        c.close()
        return True

    except:
        return False

def create_signature(data):
    print "start"
    return hashlib.sha1(data).hexdigest()

def verify_signature(data,signature):
    return create_signature(data)==signature

@app.route('/shopping')
def shopping():
    if ('addr' in session.keys()) and session['addr']==request.remote_addr:
        return(render_template('1.5_shopping.html'))
    else:
        return(redirect('/login/notfound'))

@app.route('/test/',methods=["GET","POST"])
def test():
    data=request.data
    data= json.loads(data.decode('string-escape').strip('"'))
    print data
    print "Payment status"
    return json.dumps({"status":True}),200,{'ContentType':'application/json'}

@app.route('/payment',methods=['GET','POST'])
def payment():
    if ('addr' in session.keys()) and session['addr']==request.remote_addr:
        res=request.form
        print(res)
        payu=res['totcost']
        custID=getcustID(res,res['email'])
        txn=insertintoorder(res,custID)
        print(" ---> ",txn)
        # res["txn"]=txn
        return(render_template('payment.html',l=res,txn=txn))
    else:
        return(redirect('/login/notfound'))

def getcustID(res,mail):
    try:
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()


        for key in res:
            print(key+'->'+res[key])

        d.execute("""select customer_id from customer where email='{}' """.format(mail))
        results = d.fetchall()
        print("end")
        #print(results)
        print(results[0][0])
        c.commit()
        c.close()
        return results[0][0]

    except:
        return NULL

def insertintoorder(res,custID):
    try:
        print(res)
        print("ererere")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        print("qqqqq")
        d=c.cursor()
        print("222222")

        i=random.randint(1,1000)
        #d.execute("""insert into customer values({},'dsddsdsroot','a@gmail.in','779sds88','sasrootsdss','srootsdsdssdasa','asaas');""".format(i))
        #print("-------------------------")
        #print("insert into customer(name,email,password,contact_no,occupation,address) values('{0}','{1}','{2}','{3}','{4}','{5}')".format(val[0],val[1],val[2],val[3],val[4],val[5]));
        d.execute("""insert into orders(order_id,customer_id,order_status,order_date,billingname,order_type,order_delivery_status) values({},{},{},'{}','{}',{},{})""".format(i,custID,1,res['date'],res['billingname'],res['type'],0))
        c.commit()
        for key in res:
            if res[key]=="on" and res['type']=="1":
                d.execute("""select item_id from sanitary_item where item_name='{}' """.format(key))
                r=d.fetchall()
                d.execute("""insert into includes_2(order_id,product_id) values({},{})""".format(i,r[0][0]))
                c.commit()
                print("abhi bhi")
                print(r[0][0])
                d.execute("""update sanitary_item set current_stock=current_stock-{} where item_name='{}' """.format(res[str(r[0][0])],key))
                c.commit()
            elif res[key]=="on" and res['type']=="2":
                print("saahi")
                print(res,res[key])
                d.execute("""select item_id from building_material where item_name='{}' """.format(key))
                r=d.fetchall()
                d.execute("""insert into includes_1(order_id,product_id) values({},{})""".format(i,r[0][0]))
                c.commit()
                print("abhi bhi")
                print(r[0][0])
                d.execute("""update building_material set current_stock=current_stock-{} where item_name='{}' """.format(res[str(r[0][0])],key))
                c.commit()

        print("---")




        print("end")
        c.commit()
        c.close()
        return i

    except:
        return False


@app.route('/logout/')
def logoout():
    session.pop("email",None)
    session.pop("addr",None)
    return "logged out"

@app.route('/login/notfound')
def notfound():
    return render_template('notFound.html')


@app.route('/login/profile',methods=['GET','POST'])
def profile():
    if ('addr' in session.keys()) and session['addr']==request.remote_addr:
        #session.pop("email",None)
        #session.pop("addr",None)
        print("-->  ",p)
        k=p[0]
        #k=(1,'s')
        print("saahi   ",k)
        return(render_template('1.8_profile.html',l=k))
    res=request.form
    print(res)
    if res:
        l=getCustDetail(res)
        if l!=():
            print("hey getcusID returns",l)
            # print(create_signature(res['password1']),l[0][3])
            print("started")
            if verify_signature(res['password1'],l[0][3]):
                print("ended")
                session['email']=res['email1']
                session['addr']=request.remote_addr
                print("LOGGED IN")
                print("Values of l are:")
                print(l)
                p.append(l)
                lis.append(l[0][2])
                print("*******     ",p)
                return(render_template('1.8_profile.html',l=l))
        else:
            return redirect('/login/notfound')
    return redirect('/login/notfound')


def getCustDetail(res):
    try:
        print("ererere")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        print("ddddddd")
        d=c.cursor()
        d.execute("""select * from customer where email='{}' """.format(res['email1']))
        results = d.fetchall()
        print("end")
        print(results)
        c.commit()
        c.close()
        return results
    except:
        return NULL

#------------

@app.route('/login/profile/history')
def profile_his():
    if 'addr' in session.keys() and session['addr']==request.remote_addr:
        k=p[0][0][0]
        print("sahhi    ->   ",k)
        result=getOrders(k)
        if result:
            print(result)
        return(render_template('1.8_profile_his.html',l=result))
    else:
        return(redirect('/login/notfound'))
    #return(render_template('1.8_profile_his.html'))

def getOrders(k):
    try:
        print("ererere")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        print("ddddddd")
        d=c.cursor()
        d.execute("""select * from orders where customer_id={} """.format(k))
        results = d.fetchall()
        print("end")
        print(results)
        c.commit()
        c.close()
        return results
    except:
        return NULL


@app.route('/login/profile/edit')
def profile_edit():
    if 'addr' in session.keys() and session['addr']==request.remote_addr:
        k1=p[0]
        return(render_template('1.8_profile_edit.html',l=k1))
    else:
        return(redirect('/login/notfound'))
        #return(render_template('1.8_profile_edit.html'))



#-------------------------------------------------------------------------------
@app.route('/shopping/sanitary_order')
def sanitary_order():
    if 'addr' in session.keys() and session['addr']==request.remote_addr:
        l1=func1()
        print(l1)
        l2=func2()
        return(render_template('1.6_order.html',l=l1,l2=l2,lis=lis))
    else:
        return(redirect('/login/notfound'))

def func1():
    try:
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        d.execute("""select item_id,item_name,cost,current_stock,threshold from sanitary_item """)
        results = d.fetchall()
        print("end")
        print(results)
        c.commit()
        c.close()
        return results
    except:
        return False

def func2():
    try:
        print("ererere")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        print("ddddddd")
        d=c.cursor()
        d.execute("""select email from customer """)
        results = d.fetchall()
        print("end")
        print(results)
        c.commit()
        c.close()
        return results
    except:
        return False
#-------------------------------------------------------------------------------
@app.route('/shopping/building_material',methods=['GET','POST'])
def building_order():
    if 'addr' in session.keys() and session['addr']==request.remote_addr:
        l1=func3()
        print(l1)
        l2=func4()
        return(render_template('1.6_bmorder.html',l=l1,lis=lis))
    else:
        return(redirect('/login/notfound'))
        #return(render_template('1.6_bmorder.html'))

def func3():
    try:
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        d=c.cursor()
        d.execute("""select item_id,item_name,cost,current_stock,threshold from building_material """)
        results = d.fetchall()
        print("end")
        print(results)
        c.commit()
        c.close()
        return results
    except:
        return False

def func4():
    try:
        print("ererere")
        c=connect("dg97.mysql.pythonanywhere-services.com","dg97","github!1!1","dg97$project")
        print("ddddddd")
        d=c.cursor()
        d.execute("""select email from customer """)
        results = d.fetchall()
        print("end")
        print(results)
        c.commit()
        c.close()
        return results
    except:
        return False



#-------------------------------------------------------------------------------
#example
@app.route('/<name>')
def further(name):
    return 'So hello %s how are you' %name

if(__name__=='__main__'):
    app.secret_key='secret123'
    app.run(debug=True)
