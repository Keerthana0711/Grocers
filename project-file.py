import sqlite3
import re
con=sqlite3.connect('dbproj_new.db')
cur=con.cursor()
def createtables():
    cur.execute('''CREATE TABLE IF NOT EXISTS login
              (username text UNIQUE PRIMARY KEY, dob text, password text UNIQUE )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS userinfo
            (userid text unique references login(username),name text,members number,mobileno number,doorno number,streetname text,area text)''')
    cur.execute('''CREATE TABLE if not exists daily_needs
            (userid text unique references login(username), milk number, eggs real, newspaper number, drinking_water number)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS monthly_needs
            (userid text unique references login(username), oil number, rice number, flour number, detergents number)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS stock (oil number, rice number, detergents number)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS bill (userid text unique references login(username), 
            bill_no INTEGER PRIMARY KEY AUTOINCREMENT, bill_amt number, bill_date text)''')
    con.commit()
    return

# declaring the user id variable
global uid

def newuserlogin():
    global uid
    dob = input("Enter date of birth : ")
    print('''The username must be of the length 8 to 20, may contain upper case, lower case, digit 
              and contain special character _''')
    flag1=0
    uid = input("Enter username : ")
    if re.match(r'^(?![])(?!.*[]{2})[\w.-]{8,20}(?<![_])$',uid):
        flag1 = 1
    else:
        print("The entered username does not satisfy the conditions. Please try again. ")

    if (flag1 == 1):
        print('''The password must be of the length 12 to 20, at least one upper case, one lower case, one digit 
              and may or may not contain special character _''')
        pwd = input("Enter password : ")
        if re.match(r'^(?=.{8,20}$)(?![.])(?!.*[.]{2})[a-zA-Z0-9_]+(?<![_.])$',uid):
            flag2 = 1
        else:
            print("The entered password does not satisfy the conditions. Please try again. ")
            flag2 = 0
    if  (flag1 == 1 and flag2 ==1):
        try:
            cur.execute("""INSERT INTO login(username, dob, password) VALUES (?,?,?)"""
                    ,(uid, dob, pwd))
            con.commit()
            print('Signed Up successfully!!')
            return 1
        except:
            print("Username Exits!!")
    con.commit()
    return 0

def userlogin():
    global uid
    uid=input('Enter username: ')
    passw=input('Enter password: ')
    cur.execute('''SELECT * FROM login WHERE username=? AND password=?''',(uid,passw))
    result=cur.fetchone()
    if result:
        print('Logged In Successfully!!')
        return 1
    else:
        print('Incorrect username or password!!')
        return 0
    
def enteruserdetail():
    global uid
    n=input("Enter your name: ")
    m=int(input("Enter no. of members in you family: "))
    phno=int(input("Enter your mobile number: "))
    d=int(input("Enter door number: "))
    sname=input("Enter street name:")
    a=input("Enter area name: ")
    cur.execute("""INSERT INTO userinfo values(?,?,?,?,?,?,?)""",(uid,n,m,phno,d,sname,a))
    con.commit()
    print('Entered successfully!!!')
    return

def edituserdetail():
    global uid
    print("Choices for edit of user details:")
    print("1. Name")
    print("2. Members")
    print("3. Mobile No.")
    print("4. Door No.")
    print("5. Street Name")
    print("6. Area Name")
    choice=int(input("Enter your choice: "))
    if choice==1:
        nname=input("Enter new name: ")
        cur.execute("""UPDATE userinfo SET name=? WHERE userid=?""",(nname,uid))
        con.commit()
    elif choice==2:
        nmem=int(input("Enter new members: "))
        cur.execute("""UPDATE userinfo SET member=? WHERE userid=?""",(nmem,uid))
        con.commit()
    elif choice==3:
        nphno=int(input("Enter new mobile number: "))
        cur.execute("""UPDATE userinfo SET mobileno=? WHERE userid=?""",(nphno,uid))
        con.commit()
    elif choice==4:
        ndno=int(input("Enter new door number: "))
        cur.execute("""UPDATE userinfo SET doorno=? WHERE userid=?""",(ndno,uid))
        con.commit()
    elif choice==5:
        ns=input("Enter new street name: ")
        cur.execute("""UPDATE userinfo SET streetname=? WHERE userid=?""",(ns,uid))
        con.commit()
    elif choice==6:
        na=input("Enter new area name: ")
        cur.execute("""UPDATE userinfo SET area=? WHERE userid=?""",(na,uid))
        con.commit()
    print('Updated successfully!!')
    return

def enterdailyneeds():
    global uid
    milk = int(input("The maximum quantity is 10 litres. Enter quantity of milk in L: "))
    eggs = float(input("The maximum quantity is 3 dozens. Enter no. of eggs: "))
    newspaper = int(input("Enter name of newspaper[0.None, 1. The hindu, 2. the times of india, 3. the indian express]:"))
    water = int(input("The maximum quantity is 10. Enter no. of cans:"))
    if milk<=10 and eggs<=3 and water<=10:
        cur.execute("""INSERT INTO daily_needs(userid,milk,eggs,newspaper,drinking_water) VALUES (?,?,?,?,?)""",
                    (uid,milk,eggs,newspaper,water))
    else:
        print("Please enter correct amount!")
    print('Entered successfully!!!')
    con.commit()
    return

def editdailyneeds():
    global uid
    print("Choices for edit of user details:")
    print("1. Milk")
    print("2. Eggs")
    print("3. Newspaper")
    print("4. Water Cans")
    choice=int(input("Enter your choice: "))
    if choice==1:
        nmilk=int(input("The maximum quantity is 10 litres.Enter new quantity of milk: "))
        if nmilk<=10:
            cur.execute("""UPDATE daily_needs SET milk=? WHERE userid=?""",(nmilk,uid))
        con.commit()
    elif choice==2:
        negg=float(input("The maximum quantity is 3 dozens.Enter new eggs count: "))
        if negg<=3:
            cur.execute("""UPDATE daily_needs SET eggs=? WHERE userid=?""",(negg,uid))
        con.commit()
    elif choice==3:
        nnews=int(input("Enter new newspaper[0.None, 1. The hindu, 2. the times of india, 3. the indian express]: "))
        cur.execute("""UPDATE daily_needs SET newspaper=? WHERE userid=?""",(nnews,uid))
        con.commit()
    elif choice==4:
        nwater=int(input("The maximum quantity is 10.Enter new water can count: "))
        if nwater<=10:
            cur.execute("""UPDATE daily_needs SET drinking_water=? WHERE userid=?""",(nwater,uid))
        con.commit()
    print('Updated successfully!!')
    return

def entermonthlyneeds():
    global uid
    oil = int(input("Enter quantity of oil"))
    rice = int(input("Enter the amount of rice: "))
    flour = int(input("Enter the name of flour required:[1.Rice 2.Wheat 3.Besan 4.Maida] "))
    detergents = int(input("Enter the number of detergents: "))
    cur.execute("""INSERT INTO monthly_needs(userid,oil,rice,flour,detergents) VALUES (?,?,?,?,?)""",
                (uid,oil,rice,flour,detergents))
    print('Entered successfully!!!')
    return

def stock():
    cur.execute('''SELECT COUNT(*) FROM stock''')
    temp=cur.fetchone()
    temp=int(temp[0])
    if temp==0:
        cur.execute('''INSERT INTO stock values(150, 500, 125)''')
    else:
        cur.execute('''SELECT DATE('now')''')
        r=cur.fetchone()
        cur.execute('''select date('now','start of month')''')
        s=cur.fetchone()
        cur.execute('''SELECT time('now')''')
        t = cur.fetchone()
        if (r==s and t=='00:00:00'):
            cur.execute('''UPDATE stock set oil = 150 and rice = 500 and detergents = 125''')
    con.commit()
    return
    
# calculating bill for the day and updating daily stock
def daily_stock():
    global uid
    n = [0,5,7,6]
    cur.execute('''select milk from daily_needs where userid=?''',(uid,))
    milk=cur.fetchone()
    if milk is not None:
        milk=int(milk[0])
    cur.execute('''select eggs from daily_needs where userid=?''',(uid,))
    eggs=cur.fetchone()
    if eggs is not None:
        eggs=float(eggs[0])
    cur.execute('''select newspaper from daily_needs where userid=?''',(uid,))
    news=cur.fetchone()
    if news is not None:
        news=int(news[0])
    cur.execute('''select drinking_water from daily_needs where userid=?''',(uid,))
    water=cur.fetchone()
    if water is not None:
        water=int(water[0])
    if (milk is not None) and (eggs is not None) and (news is not None) and (water is not None):
        daily_amt=(milk*30)+(eggs*50)+(n[news])+(water*75)
        cur.execute('''select date('now')''')
        r_date=cur.fetchone()
        r_date=str(r_date[0])
        cur.execute('''select time('now')''')
        r=cur.fetchone()
        r=str(r[0])
        if r=='08:00:00':
            cur.execute('''INSERT INTO bill(bill_amt, bill_date) values(?,?)''',(daily_amt, r_date))
            cur.execute('''select max(bill_no) from bill''')
            bno=cur.fetchone()
            bno=int(bno[0])
            print('Bill no :',bno)
            print('The total bill amount for the day is: ',daily_amt)
        con.commit()
    return

# calculating bill for the month and updating monthly stock
def monthly_stock():
    global uid
    f = [0,30,32,36,28]
    cur.execute('''select oil from monthly_needs where userid=?''',(uid,))
    oil=cur.fetchone()
    if oil is not None:
        oil=int(oil[0])
    cur.execute('''select rice from monthly_needs where userid=?''',(uid,))
    rice=cur.fetchone()
    if rice is not None:
        rice=int(rice[0])
    cur.execute('''select flour from monthly_needs where userid=?''',(uid,))
    flour=cur.fetchone()
    if flour is not None:
        flour=int(flour[0])
    cur.execute('''select detergents from monthly_needs where userid=?''',(uid,))
    detergents=cur.fetchone()
    if detergents is not None:
        detergents=int(detergents[0])
    if (oil is not None) and (rice is not None) and (flour is not None) and (detergents is not None):
        mon_amt = (oil*45)+(rice*32)+(f[flour])+(detergents)
        cur.execute('''select date('now')''')
        r=cur.fetchone()
        r=str(r[0])
        cur.execute('''select date('now','start of month')''')
        s=cur.fetchone()
        s=str(s[0])
        if r==s:
            cur.execute('''INSERT INTO bill(bill_amt, bill_date) values(?,?)''',(mon_amt, r))
            cur.execute('''select max(bill_no) from bill''')
            bno=cur.fetchone()
            bno=int(bno[0])
            print('Bill no :',bno)
            print("The total bill amount for the month is ",mon_amt)
            cur.execute('''SELECT oil from stock''')
            oil1 = cur.fetchone()
            oil1=int(oil1[0])
            cur.execute('''SELECT rice from stock''')
            rice1 = cur.fetchone()
            rice1=int(rice1[0])
            cur.execute('''SELECT detergents from stock''')
            det1 = cur.fetchone()
            det1=int(det1[0])
            if (oil1>=oil and rice1>=rice and det1>=detergents):
                oil1=oil1-oil
                rice1=rice1-rice
                det1=det1-detergents
                cur.execute('''UPDATE stock set oil = ?''', (oil1,))
                cur.execute('''UPDATE stock set rice = ?''', (rice1,))
                cur.execute('''UPDATE stock set detergents = ?''', (det1,))
        con.commit()
    return

createtables()
print("------Log In/Sign Up------")
print("Enter 1 for Sign Up In\n Enter 2 for Log In")
ch=int(input())
if ch==1:
    res=newuserlogin()
else:
    res=userlogin()

if (res==1):
    ch1=input('Do you want to continue? if yes press y or Y ')
    while(ch1=='y' or ch1=='Y'):
        print("1. Enter user details\n2.Edit user details\n3.Enter daily needs\n4.Edit daily needs\n5.Enter monthly needs")
        choose=int(input('Enter your choice: '))
        if choose==1:
            enteruserdetail()
        elif choose==2:
            edituserdetail()
        elif choose==3:
            enterdailyneeds()
        elif choose==4:
            editdailyneeds()
        elif choose==5:
            entermonthlyneeds()
        ch1=input('Do you want to continue? if yes press y or Y ')

# filling up the stock
stock()

daily_stock()

monthly_stock()

con.close()
print('----------Thank You!!----------')
