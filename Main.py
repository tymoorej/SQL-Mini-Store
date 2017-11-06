import sqlite3
import sys
from getpass import getpass
from collections import Counter
from datetime import *

connection = None
cursor = None
user = None
basket= dict()
uOrder = 1
uDelivery = 1

class Customer(object):
    def __init__(self, username, password):
        self.password = password
        self.username = username
class Agent(Customer):
    def __init__(self, username, name, password):
        super().__init__(username, password)
        self.name = name
class RCustomer(Customer):
    def __init__(self, username, name, address, password):
        super().__init__(username, password)
        self.name = name
        self.address = address


#### MARK: Setup Functions

def setup():
    global connection, cursor
    db = sys.argv[1]
    if db is None:
        return -1
    connection = sqlite3.connect("./" + db)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()

def setup_test():
    global connection, cursor
    connection = sqlite3.connect("./store.db")
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()

def define_tables():
    global connection, cursor
    drop_tables='''
    drop table if exists deliveries;
    drop table if exists olines;
    drop table if exists orders;
    drop table if exists customers;
    drop table if exists carries;
    drop table if exists products;
    drop table if exists categories;
    drop table if exists stores;
    drop table if exists agents;
    '''

    create_tables='''
    create table agents (
      aid           text,
      name          text,
      pwd       	text,
      primary key (aid));
    create table stores (
      sid		int,
      name		text,
      phone		text,
      address	text,
      primary key (sid));
    create table categories (
      cat           char(3),
      name          text,
      primary key (cat));
    create table products (
      pid		char(6),
      name		text,
      unit		text,
      cat		char(3),
      primary key (pid),
      foreign key (cat) references categories);
    create table carries (
      sid		int,
      pid		char(6),
      qty		int,
      uprice	real,
      primary key (sid,pid),
      foreign key (sid) references stores,
      foreign key (pid) references products);
    create table customers (
      cid		text,
      name		text,
      address	text,
      pwd		text,
      primary key (cid));
    create table orders (
      oid		int,
      cid		text,
      odate		date,
      address	text,
      primary key (oid),
      foreign key (cid) references customers);
    create table olines (
      oid		int,
      sid		int,
      pid		char(6),
      qty		int,
      uprice	real,
      primary key (oid,sid,pid),
      foreign key (oid) references orders,
      foreign key (sid) references stores,
      foreign key (pid) references products);
    create table deliveries (
      trackingNo	int,
      oid		int,
      pickUpTime	date,
      dropOffTime	date,
      primary key (trackingNo,oid),
      foreign key (oid) references orders);
    '''

    cursor.executescript(drop_tables)
    cursor.executescript(create_tables)
    connection.commit()

def insert_data():
    global connection, cursor

    #agents(aid, name, pwd)
    insertions_agent = [
    ('a007', 'James Bond', '007'),]
    cursor.executemany("INSERT INTO agents VALUES (?,?,?)",insertions_agent),

    # categories(cat, name)
    insertions_cat = [
    ('dai', 'Dairy'),
    ('bak', 'Bakery'),
    ('pro', 'Produce'),
    ('ele', 'Electronics'),
    ('clo', 'Clothing and Apparel'),
    ('hom', 'Home Appliances'),
    ('toy', 'Childrens section'),
    ('kid', 'Kids Clothing and Apparel'),
    ('car', 'Autoshops'),]
    cursor.executemany("INSERT INTO categories VALUES (?,?)",insertions_cat),

    # products(pid, name, unit, cat)
    insertions_products = [
    ('p10','4L milk 1%','ea', 'dai'),
    ('p20','dozen large egg','ea', 'dai'),
    ('p30','cheddar cheese (270g)','ea', 'dai'),
    ('p40','white sliced bread','ea', 'bak'),
    ('p50','dozen donuts','ea', 'bak'),
    ('p60','red delicious apple','lb', 'pro'),
    ('p70','gala apple','lb', 'pro'),
    ('p80','baby carrots (454g)','ea', 'pro'),
    ('p90','broccoli','lb', 'pro'),
    ('p100','headphones','ea', 'ele'),
    ('p110','8gb sdhc Card','ea', 'ele'),
    ('p120','aaa batteries (8-pk)','ea', 'ele'),
    ('p130','led hd tv, 32-in','ea', 'ele'),
    ('p140','v-neck sweater','ea', 'clo'),
    ('p150','cotton hoodie','ea', 'clo'),
    ('p160','coffee maker','ea', 'hom'),
    ('p170','toaster','ea', 'hom'),
    ('p180','food mixer','ea', 'hom'),]
    cursor.executemany("INSERT INTO products VALUES	(?, ?, ?, ?)",	insertions_products),

    # customers(cid, name, address, pwd)
    insertions_cust = [('c1','Bob', '12345 Ave', 'ezpass'),
    ('c2', 'Joe', '13 Street', 'pass'),
    ('c10', 'Jack Abraham', 'CS Dept, University of Alberta', 'flower'),
    ('c20', 'Joe Samson', '9632-107 Ave','lily'),
    ('c30', 'John Connor', '111-222 Ave','house'),
    ('c40', 'Sam Tritzen', '9702-162 St NW','sun'),
    ('c50', 'Bryanna Petrovic', '391 Richfield Rd','sunrise'),
    ('c60', 'John Doe', '11 Knottwood Rd','hello'),
    ('c70', 'Jane Donald', '8012-122 St SW','howareyou'),
    ('c80', 'Erin Branch', '54 Elanore Dr','fuckthis'),
    ('c90', 'Johnathon Doe', '11 Knottwood Rd','tyistheworst'),
    ('c91', 'Donald Donald', '812-122 St SW','heyLuke'),
    ('c92', 'Donald Trump', '64 Elanore Dr','whatsup'),]
    cursor.executemany("INSERT INTO customers VALUES (?,?,?,?)",insertions_cust),

    # stores(sid, name, phone, address)
    insertion_stores=[
    (10, 'Canadian Tire', '780-111-2222', 'Edmonton South Common'),
    (20, 'Walmart', '780-111-3333', 'Edmonton South Common'),
    (30, 'Loblaw City Market', '780-428-1945', 'Oliver Square'),
    (40, 'Shoppers Drug Mart', '780-426-7642', 'Edmonton City Centre'),
    (50, 'Shoppers Drug Mart', '780-474-8237', 'Kingsway Mall'),
    (60, 'Sears Department Store', '780-438-2098', 'Southgate Centre'),
    (70, 'Hudsons Bay', '780-435-9211', 'Southgate Centre'),
    (80, 'abc', '780-479-8937', 'abc Mall'),
    (90, 'def', '780-478-2098', 'def Centre'),
    (100, 'ghi', '780-436-9212', 'Southgate Centre'),
    (110, 'lmn', '780-112-2222', 'Edmonton South Common'),
    (120, 'opq', '780-113-3333', 'Edmonton South Common'),
    (130, 'rst', '780-429-1945', 'Oliver Square'),]
    cursor.executemany("INSERT INTO stores VALUES (?,?,?,?)",insertion_stores),

    # carries(sid, pid, qty, uprice)
    insertions_carriers =[
    (10, 'p110', 75, 13.99),
    (10, 'p120', 50, 12.99),
    (10, 'p130', 20, 249.99),
    (10, 'p160', 35, 24.99),
    (10, 'p170', 40, 19.99),
    (20, 'p10', 100, 4.70),
    (20, 'p20', 80, 2.60),
    (20, 'p30', 60, 3.79),
    (20, 'p40', 120, 2.20),
    (20, 'p50', 40, 4.00),
    (20, 'p60', 100, 0.79),
    (20, 'p70', 90, 1.15),
    (20, 'p90', 0, 1.79),
    (20, 'p100', 20, 11.79),
    (30, 'p10', 90, 4.60),
    (30, 'p30', 0, 3.75),
    (30, 'p40', 100, 2.10),
    (30, 'p50', 35, 5.99),
    (30, 'p60', 98, 1.05),
    (30, 'p70', 68, 1.25),
    (30, 'p80', 40, 1.99),
    (30, 'p90', 70, 1.79),
    (30, 'p160', 30, 24.99),
    (40, 'p10', 90, 4.75),
    (40, 'p20', 70, 2.40),
    (40, 'p30', 40, 3.89),
    (40, 'p40', 89, 1.99),
    (40, 'p60', 100, 0.79),
    (40, 'p120', 0, 2.99),
    (50, 'p10', 80, 4.75),
    (50, 'p20', 80, 2.40),
    (50, 'p30', 38, 3.89),
    (50, 'p40', 84, 1.99),
    (50, 'p120', 4, 12.99),
    (60, 'p110', 50, 14.39),
    (60, 'p120', 75, 13.99),
    (60, 'p170', 50, 19.99),
    (60, 'p100', 20, 13.49),
    (70, 'p140', 32, 22.99),
    (70, 'p150', 28, 54.99),
    (70, 'p100', 9, 17.59),
    (80, 'p110', 75, 13.99),
    (80, 'p120', 50, 12.99),
    (80, 'p130', 20, 249.99),
    (80, 'p160', 35, 24.99),
    (90, 'p170', 40, 19.99),
    (90, 'p10', 100, 4.70),
    (90, 'p20', 80, 2.60),
    (90, 'p30', 60, 3.79),
    (110, 'p40', 120, 2.20),
    (110, 'p50', 40, 4.00),
    (110, 'p60', 100, 0.79),
    (120, 'p70', 90, 1.15),
    (120, 'p90', 0, 1.79),
    (120, 'p100', 20, 11.79),
    (130, 'p10', 90, 4.60),
    (130, 'p30', 0, 3.75),
    (130, 'p40', 100, 2.10),
    (130, 'p50', 35, 5.99),
    (130, 'p60', 98, 1.05),]
    cursor.executemany("INSERT INTO carries VALUES (?,?,?,?)",insertions_carriers),


    # orders(oid, cid, odate, address)
    insertions_orders = [
    (100, 'c10', datetime.now(), 'Athabasca Hall, University of Alberta'),
    (110, 'c40', datetime.now(), '9702-162 St NW'),
    (120, 'c20', datetime(2017, 11, 18), '9632-107 Ave'),
    (130, 'c60', datetime(2017, 10, 8), '31 Jackson Ave'),
    (140, 'c40', datetime(2017, 10, 15), '9702-162 St NW'),
    (150, 'c40', datetime(2017, 9, 27), '9702-162 St NW'),
    (160, 'c50', datetime(2016, 8, 5), '391 Richfield Rd'),
    (170, 'c10', datetime(2016, 8, 6), 'Athabasca Hall, University of Alberta'),
    (180, 'c20', datetime(2015, 9, 21), '9632-107 Ave'),
    (190, 'c50', datetime(2013, 7, 29), '391 Richfield Rd'),
    (200, 'c70', datetime(2013, 6, 17), '90 Jonah Ave'),
    (210, 'c70', datetime(2018, 10, 23), '8012-122 St SW'),
    (220, 'c80', datetime(2012, 3, 6), '54 Elanore Dr'),
    (230, 'c30', datetime(2011, 4, 6), '111-222 Ave'),]
    cursor.executemany("INSERT INTO orders VALUES (?,?,?,?)",insertions_orders),

    # olines(oid, sid, pid, qty, uprice)
    insertions_olines = [
    (100, 20, 'p20', 1, 2.8),
    (110, 30, 'p70', 1, 1.25),
    (110, 30, 'p80', 2, 1.99),
    (120, 20, 'p10', 1, 4.7),
    (120, 40, 'p20', 1, 2.4),
    (120, 40, 'p30', 1, 3.89),
    (130, 70, 'p150', 1, 54.99),
    (140, 40, 'p60', 2, 0.79),
    (140, 30, 'p90', 2, 1.79),
    (150, 60, 'p110', 1, 14.39),
    (160, 20, 'p70', 1, 1.15),
    (160, 30, 'p80', 1, 1.99),
    (170, 20, 'p100', 2, 11.79),
    (180, 40, 'p60', 1, 0.79),
    (180, 40, 'p120', 1, 12.99),
    (180, 40, 'p40', 1, 1.99),
    (190, 20, 'p50', 1, 4),
    (190, 20, 'p10', 1, 4.7),
    (200, 10, 'p130', 1, 249.99),
    (210, 10, 'p120', 1, 12.99),
    (220, 30, 'p10', 1, 4.6),
    (230, 20, 'p50', 2, 4),]
    cursor.executemany("INSERT INTO olines VALUES (?,?,?,?,?)",insertions_olines),

    # deliveries(trackingno, oid, pickUpTime, dropOffTime)
    insertions_deliveries =[
    (1000,100,datetime.now(), None),
    (1001,110,datetime.now(), datetime(2016, 11, 18)),
    (1002,120,datetime(2017, 9, 18), datetime(2017, 10, 18)),
    (1003,130,datetime(2016, 10, 18), None),
    (1004,140,datetime(2016, 9, 18), datetime(2016, 12, 18)),
    (1005,150,datetime(2015, 1, 18), None),
    (1006,160,datetime(2015, 2, 18), None),
    (1007,170,datetime(2014, 3, 18), datetime(2015, 1, 18)),
    (1008,180,datetime(2014, 4, 18), None),
    (1009,190,datetime(2014, 5, 18), datetime(2014, 12, 18)),
    (1010,200,datetime(2014, 6, 18), None),
    (1011,210,datetime(2014, 7, 18), datetime(2014, 10, 18)),
    (1012,220,datetime(2013, 8, 18), None),
    (1013,230,datetime(2012, 9, 18), None),]
    cursor.executemany("INSERT INTO deliveries VALUES (?,?,?,?)",insertions_deliveries),

#### MARK: Search functions
def search_for_keyword(keywords):
    results=get_base(keywords)
    results=add_onto_base(results)

    return results

def get_base(keywords):
    global connection, cursor
    keyword_list=keywords.split(" ")
    results=[]
    for key in keyword_list:
        k="%"+key+"%"
        cursor.execute('''
        SELECT p.pid, p.name, p.unit, COUNT(DISTINCT c.sid)
        FROM products p, carries c
        WHERE p.pid=c.pid AND p.name LIKE ?
        GROUP BY p.pid, p.name, p.unit
         '''
        ,[k])
        rows=cursor.fetchall()
        results=results+rows

    results.sort(key=Counter(results).get, reverse=True)
    list1 = results
    list2 = sorted(set(list1),key=list1.index)
    results=list2
    return results

def add_onto_base(results):
    global connection, cursor
    for i in range(len(results)):
        p=results[i][0]

        cursor.execute('''
        SELECT COUNT(DISTINCT c.sid)
        FROM products p, carries c
        WHERE p.pid=c.pid AND p.pid=? AND c.qty>0
        GROUP BY p.pid, p.name, p.unit
         '''
        ,[p])
        rows=cursor.fetchall()
        if len(rows)!=0:
            results[i]=results[i]+(rows[0][0],)
        else:
            results[i]=results[i]+(0,)




        cursor.execute('''
        SELECT MIN(c.uprice)
        FROM products p, carries c
        WHERE p.pid=c.pid AND p.pid=?
         '''
        ,[p])
        rows=cursor.fetchall()
        results[i]=results[i]+(rows[0][0],)



        cursor.execute('''
        SELECT MIN(c.uprice)
        FROM products p, carries c
        WHERE p.pid=c.pid AND p.pid=? AND c.qty>0
         '''
        ,[p])
        rows=cursor.fetchall()
        if len(rows)!=0:
            results[i]=results[i]+(rows[0][0],)
        else:
            results[i]=results[i]+(0,)




        cursor.execute('''
        SELECT COUNT(DISTINCT o.oid)
        FROM products p, orders o, olines ol
        WHERE p.pid=ol.pid AND o.oid=ol.oid AND p.pid=? AND date(o.odate, '+7 day') >= date('now')
         '''
        ,[p])
        rows=cursor.fetchall()
        results[i]=results[i]+(rows[0][0],)



    return results

def csearch() :
    """
    Tymoore's search function
    """
    global cursor
    keywords=input("Please enter your space seperated keywords: ")
    results=search_for_keyword(keywords)
    sPrint("")

    LAYOUT = "{!s:15} {!s:25} {!s:20} {!s:15} {!s:25} {!s:15} {!s:25} {!s:15}"

    if len(results)==0:
        print("There are no results that match.")

    elif len(results)<5:
        print(LAYOUT.format("Product ID","Product Name","Product Unit","# of Stores","# of Stores(in stock)","Min Price","Min Price(in stock)","Orders in last week"))
        for i in range(len(results)):
            print(LAYOUT.format(*results[i]))
        sPrint("")


        while True:
            row_index = int(input("Select the number of the row you would like to know more about (NOTE row starts at 0): "))

            if(row_index>=len(results) or row_index<0):
                print("Sorry that row does not exist please try again")
            else:
                more_info(results[row_index][0])
                break
    else:
        times_moved=0
        while True:
            minimum=min(times_moved*5+5,len(results))

            if(times_moved*5+5<len(results)):
                sPrint("")
                print(LAYOUT.format("Product ID","Product Name","Product Unit","# of Stores","# of Stores(in stock)","Min Price","Min Price(in stock)","Orders in last week"))
                for i in range(times_moved*5,minimum):
                    print(LAYOUT.format(*results[i]))
                scroll=int(input("Select 1 to see more rows or 0 to examine these rows further: "))
                if scroll==1:
                    times_moved=times_moved + 1
                    continue
                elif scroll==0:
                    pass
                else:
                    should_continue=0
                    while True:
                        print("Please select either 0 or 1")
                        scroll=int(input("Select 1 to see more rows or 0 to examine these rows further: "))
                        if scroll==0:
                            break
                        elif scroll==1:
                            times_moved=times_moved + 1
                            should_continue=1
                            break
                    if should_continue:
                        continue

            else:
                sPrint("")
                print(LAYOUT.format("Product ID","Product Name","Product Unit","# of Stores","# of Stores(in stock)","Min Price","Min Price(in stock)","Orders in last week"))
                for i in range(times_moved*5,len(results)):
                    print(LAYOUT.format(*results[i]))

            row_index = int(input("Select the number of the row you would like to know more about (NOTE row starts at 0): "))

            minimum=min(times_moved*5+5,len(results))
            if(row_index>=(minimum-times_moved*5) or row_index<0):
                print("Sorry that row does not exist please try again")
            else:
                more_info(results[times_moved*5+row_index][0])
                break


    sPrint("")

def more_info(pid):
    global connection, cursor
    cursor.execute('''
    SELECT p.pid, p.name, p.unit, p.cat
    FROM products p
    WHERE p.pid=?
     '''
    ,[pid])
    rows=cursor.fetchall()

    print("\n\n\n" + pid + "'s info can be found below:\n\n")
    LAYOUT = "{!s:15} {!s:25} {!s:20} {!s:15}"
    print(LAYOUT.format("Product ID","Product Name","Product Unit","Product Category"))
    print(LAYOUT.format(*rows[0]))

    print("\n\n"+pid + " can be found in the following stores:\n\n")
    print("In stock:\n\n")

    # TODO: Fix queries- MAYBE????? BARE MINIMUM: ALOT MORE TESTING
    cursor.execute('''
    SELECT c.sid, c.qty, c.uprice, COUNT(DISTINCT ol.oid)
    FROM (carries c, orders o) LEFT OUTER JOIN olines ol using (sid,pid,oid)
    WHERE c.pid=? AND c.qty>0 and date(o.odate, '+7 day') >= date('now')
    GROUP BY c.sid, c.qty, c.uprice
     '''
    ,[pid])
    rows=cursor.fetchall()
    LAYOUT = "{!s:10} {!s:10} {!s:12} {!s:18}"
    print(LAYOUT.format("Store ID","Quantity","Unit Price","Bought in last week"))
    if len(rows) != 0:
        for i in range(len(rows)):
            print(LAYOUT.format(*rows[i]))
    else:
        print("No Results\n")


    print("\n\nNot in stock:\n\n")

    cursor.execute('''
    SELECT c.sid, c.qty, c.uprice, COUNT(DISTINCT ol.oid)
    FROM (carries c, orders o) LEFT OUTER JOIN olines ol using (sid,pid,oid)
    WHERE c.pid=? AND c.qty=0 and date(o.odate, '+7 day') >= date('now')
    GROUP BY c.sid, c.qty, c.uprice
     '''
    ,[pid])
    rows2=cursor.fetchall()
    LAYOUT = "{!s:10} {!s:10} {!s:12} {!s:18}"
    if len(rows2) != 0:
        print(LAYOUT.format("Store ID","Quantity","Unit Price","Bought in last week"))
        for i in range(len(rows2)):
            print(LAYOUT.format(*rows2[i]))
    else:
        print("No Results")


    if len(rows)==0:
        print()
        print()
        print()

        print("Sorry you cannot order that product because no store has it in stock")
        return

    order = input("\n\nWould you like to order any of these options(From the in stock stores)? [y/n] ").lower()
    if order == 'y':
        choice = int(input("Select the number of the row(From the in stock stores) you would like to know more about (NOTE row starts at 0): "))
        while choice >= len(rows) or choice < 0:
            print("Please choose a valid row")
            choice = int(input("Select the number of the row(From the in stock stores) you would like to know more about (NOTE row starts at 0): "))
        qty=1
        check = input("\n\nThe default order quantity is 1, would you like to change it? [y/n] ").lower()
        if check == 'y':
            qty= int(input("How many do you want? (note min is 1) "))
            while qty<1:
                print("Please choose a quantity greater than or equal to 1")
                qty= int(input("How many do you want? (note min is 1) "))


        addtoBasket(pid, rows[choice][0], rows[choice][2], qty)


#### MARK: Order functions
def fillBasket():
    global basket
    basket[('p10',30,4.60)] = 2
    basket[('p110',10,13.99)] = 1

def checkBasket():
    global basket
    for keys in basket:
        print(keys,basket[keys])

def addtoBasket(pid, sid, uprice, qty):
    global basket
    if (pid,sid,uprice) in basket:
        basket[(pid,sid,uprice)]+=qty
    else:
        basket[(pid, sid, uprice)] = qty
    print()
    print("Your basket is now: ", basket)
    print()


def checkOrders():
    """
    Just a testing function
    """
    global cursor
    cursor.execute(""" SELECT * FROM olines""")
    ol=cursor.fetchall()
    cursor.execute(""" SELECT * FROM orders""")
    o=cursor.fetchall()
    print(ol)
    print(o)

def checkCarries():
    global cursor
    cursor.execute(""" SELECT * FROM carries""")
    c=cursor.fetchall()
    print(c)

def placeOrder():
    global user,basket, uOrder, cursor, connection

    cursor.execute(""" SELECT max(oid) FROM orders """)
    uOrder=cursor.fetchall()[0][0] + 10
    order = []
    for items in basket:
        pid, sid, uprice = items
        qty = basket[items]
        cursor.execute(""" SELECT qty FROM carries WHERE sid=? AND pid=?""", [sid, pid])
        realQty=cursor.fetchall()
        cursor.execute("""SELECT name FROM stores WHERE sid=?""", [sid])
        sname = cursor.fetchall()
        cursor.execute("""SELECT name FROM products WHERE pid=?""", [pid])
        pname = cursor.fetchall()
        if qty > realQty[0][0]:
            print("The store " + sname[0][0] + " only has " + str(realQty[0][0]) + " " + pname[0][0] + "s. ")
            choice = int(input("Would you like to: \n1.Change the quantity? \n 2.Delete product from basket?\n"))
            if choice == 1:
                print("Maximum quantity: ", realQty[0][0])
                qty = int(input("What is your new quantity? "))
                while qty > realQty[0][0] or qty<0:
                    print("Please select a quantity lesser than or equal to the max quantity and greater than or equal to zero")
                    qty = int(input("What is your new quantity? "))
                cursor.execute("""UPDATE carries
                                SET qty = qty - ?
                                WHERE sid=? AND pid=?""", [qty,sid,pid])
                connection.commit()
                order.append((uOrder,sid,pid,qty,uprice))
            elif choice == 2:
                del basket[(pid,sid,uprice)]
        else :
            cursor.execute("""UPDATE carries
                            SET qty = qty - ?
                            WHERE sid=? AND pid=?""", [qty,sid,pid])
            connection.commit()
            order.append((uOrder,sid,pid,qty,uprice))

    # Creating new orders
    """orders(oid, cid, odate, address) olines(oid, sid, pid, qty, uprice)"""
    cursor.execute("INSERT INTO orders VALUES (?,?,?,?)",(uOrder,user.username,datetime.today(),user.address)),
    cursor.executemany("INSERT INTO olines VALUES (?,?,?,?,?)",order),

#### MARK: Agent options
# orders(oid, cid, odate, address)

def checkDeliveries():
    """
    Just a testing function
    """
    global cursor

    cursor.execute(""" SELECT * FROM deliveries""")
    d=cursor.fetchall()
    print(d)

def setupDeliveries():
    global user, uDelivery, cursor, connection

    cursor.execute(""" SELECT max(trackingNo) FROM deliveries """)
    uDelivery=cursor.fetchall()[0][0] + 1
    deliveries = []

    cursor.execute(""" SELECT * FROM orders""")
    ordersList = cursor.fetchall()
    times_moved=0
    while True:
        minimum=min(times_moved*5+5,len(ordersList))

        if(times_moved*5+5<len(ordersList)):
            sPrint("")
            LAYOUT = "{!s:10} {!s:12} {!s:30} {!s:20}"
            print(LAYOUT.format("Order ID","Customer ID","Order Date","Address"))
            for i in range(times_moved*5,minimum):
                print(LAYOUT.format(*ordersList[i]))
            scroll=int(input("Select 1 to see more rows or 0 to examine these rows further: "))
            if scroll==1:
                times_moved=times_moved + 1
                continue
            elif scroll==0:
                pass
            else:
                should_continue=0
                while True:
                    print("Please select either 0 or 1")
                    scroll=int(input("Select 1 to see more rows or 0 to examine these rows further: "))
                    if scroll==0:
                        break
                    elif scroll==1:
                        times_moved=times_moved + 1
                        should_continue=1
                        break
                if should_continue:
                    continue

        else:
            sPrint("")
            print(LAYOUT.format("Order ID","Customer ID","Order Date","Address"))
            for i in range(times_moved*5,len(ordersList)):
                print(LAYOUT.format(*ordersList[i]))
        anotherOne = input("Do you want to add an order to your a delivery? [y/n]: ").lower()

        while anotherOne == 'y':
            row_index = int(input("Select the number of the row you would like to add to the delivery (NOTE row starts at 0): "))
            minimum=min(times_moved*5+5,len(ordersList))
            if(row_index>=(minimum-times_moved*5) or row_index<0):
                print("Sorry that row does not exist please try again")
            else:
                pckup = input("Add a pickup time (in format 'YYYY MM DD'). Type 'no' for no date: ")
                try:
                    pckup = datetime.strptime(pckup, '%Y %m %d')
                except ValueError:
                    pckup = None
                deliveries.append((ordersList[times_moved*5+row_index][0],pckup)) # datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
                anotherOne = input("Do you want to add another order to your a delivery? [y/n]: ").lower()

        for deliv in deliveries:
            cursor.execute("INSERT INTO deliveries VALUES (?,?,?,?)",[uDelivery,deliv[0],deliv[1], None]),
        connection.commit()
        break

def updateDelivery():
    global cursor
    # deliveries(trackingno, oid, pickUpTime, dropOffTime)
    tNo = int(input("Which delivery do you want to view? "))
    cursor.execute(""" SELECT * FROM deliveries WHERE trackingNo=?""", [tNo])
    deliv = cursor.fetchall()
    LAYOUT = "{!s:14} {!s:10} {!s:28} {!s:15}"
    if len(deliv) == 0:
        print("That delivery does not exist...")
        return
    else:

        times_moved=0
        while True:
            minimum=min(times_moved*5+5,len(deliv))

            if(times_moved*5+5<len(deliv)):
                sPrint("")

                print(LAYOUT.format("Tracking No.","Order ID","Pickup Time","Drop Off Time"))
                for i in range(times_moved*5,minimum):
                    print(LAYOUT.format(*deliv[i]))
                scroll=int(input("Select 1 to see more rows or 0 to examine these rows further: "))
                if scroll==1:
                    times_moved=times_moved + 1
                    continue
                elif scroll==0:
                    pass
                else:
                    should_continue=0
                    while True:
                        print("Please select either 0 or 1")
                        scroll=int(input("Select 1 to see more rows or 0 to examine these rows further: "))
                        if scroll==0:
                            break
                        elif scroll==1:
                            times_moved=times_moved + 1
                            should_continue=1
                            break
                    if should_continue:
                        continue

            else:
                sPrint("")
                print(LAYOUT.format("Tracking No.","Order ID","Pickup Time","Drop Off Time"))
                for i in range(times_moved*5,len(deliv)):
                    print(LAYOUT.format(*deliv[i]))

            row_index = int(input("Select the number of the row corresponding to the order you want to pick up (NOTE row starts at 0): "))

            minimum=min(times_moved*5+5,len(deliv))
            if(row_index>=(minimum-times_moved*5) or row_index<0):
                print("Sorry that row does not exist please try again")
            else:
                editOrder(deliv[times_moved*5+row_index])
                break

def editOrder(orderTuple):
    global connection
    # deliveries(trackingno, oid, pickUpTime, dropOffTime)
    anotherOne = 'y'
    while anotherOne == 'y':
        option = int(input("Select the number corresponding to option you want:\n 1. Change the Pickup Time\n 2. Change the DropOff Time\n 3. Delete the Order\n"))
        if option not in [1,2,3]:
            print("Incorrect selection...")
        else:
            if option == 1:
                pckup = input("Add a pickup time (in format 'YYYY MM DD'): ")
                try:
                    pckup = datetime.strptime(pckup, '%Y %m %d')
                    cursor.execute("""UPDATE deliveries
                                    SET pickUpTime = ?
                                    WHERE oid=? AND trackingNo=?""" , [pckup,orderTuple[1],orderTuple[0]])
                except ValueError:
                    print("Wrong date format...")
            elif option == 2:
                dpoff = input("Add a drop off time (in format 'YYYY MM DD'): ")
                try:
                    dpoff = datetime.strptime(dpoff, '%Y %m %d')
                    cursor.execute("""UPDATE deliveries
                                    SET dropOffTime = ?
                                    WHERE oid=? AND trackingNo=?""" , [dpoff,orderTuple[1],orderTuple[0]])
                except ValueError:
                    print("Wrong date format...")
            elif option == 3:
                cursor.execute("""DELETE FROM deliveries
                                WHERE trackingNo=? AND oid=?
                                """ ,
                                [orderTuple[0],orderTuple[1]])
                connection.commit()
            else:
                print("No corresping option...")
            anotherOne = input("Do you want to make more changes? [y/n] ").lower()
    connection.commit()

def addtoStock():
    global user, cursor

    cursor.execute(""" SELECT * FROM carries """)
    prodList = cursor.fetchall()
    times_moved=0
    pid = input("Enter the pid of the product you want to edit: ").strip()
    sid = int(input("Enter the sid of the product you want to edit: "))
    cursor.execute(""" SELECT * FROM carries WHERE sid=? AND pid=?""", [sid, pid])
    rows=cursor.fetchall()
    if len(rows) != 1:
        cursor.execute(""" SELECT * FROM products WHERE pid=?""", [pid])
        prodExist =cursor.fetchall()
        cursor.execute(""" SELECT * FROM stores WHERE sid=?""", [sid])
        storeExist =cursor.fetchall()
        if len(storeExist) and len(prodExist):
            addQty = int(input("How many should be added? "))
            option = input("Do you want to add a unit price? [y/n] ")
            if option == 'y':
                addPrice = float(input("What should the new unit price be? "))
            else:
                addPrice = None
            # carries(sid, pid, qty, uprice)
            cursor.execute("INSERT INTO carries VALUES (?,?,?,?)",(sid,pid,addQty,addPrice))
            connection.commit()
        else:
            print("Invalid PID and/or SID does not exist...")
            return
    else:
        while True :
            option = int(input("Select the corresponding for your chosen option:\n 1.Add to the Stock\n 2.Change the Unit Price\n 3.Exit\n"))
            if option == 1:
                addQty = int(input("How many should be added? "))
                cursor.execute("""UPDATE carries
                                SET qty = qty + ?
                                WHERE sid=? AND pid=?""", [addQty,sid,pid])
            elif option == 2:
                addPrice = float(input("What should the new unit price be? "))
                cursor.execute("""UPDATE carries
                                SET uprice = ?
                                WHERE sid=? AND pid=?""" , [addPrice,sid,pid])
            elif option == 3:
                checkCarries()
                break
        connection.commit()




#### MARK: Menu Functions
def logout():
    global user, basket, cursor

    if user:
        print("Logout:", user.username)
    user = None
    basket = dict()


def login(userType): #cid, name, address, pwd)
    global user

    if userType == 1:
        if user is None:
            while True:
                print()
                print()
                print()
                option = int(input("Select corresponding number: \n1.Log In \n2.Sign Up \n3.Exit \n"))
                if option in [1,2]:
                    break
                elif option == 3:
                    return -2
                else:
                    print("Please select a valid number")
            error = customerLogIn(option)
            if error is not None:
                #sPrint("Invalid Log In Credentials")
                return error
    else :  # AGENT Menu
        error = agentLogin()
        if error is not None:
            #sPrint("Invalid Log In Credentials")
            return error


def agentLogin():
    global user, cursor

    print()
    print()
    print()

    username = input("Enter a valid ID. Enter exit to return: ").strip()
    if username.lower() == 'exit':
        return -2
    pas = getpass(prompt='Password: ')
    cursor.execute(""" SELECT * FROM agents WHERE aid=? AND pwd=?""", [username, pas])
    rows=cursor.fetchall()
    if len(rows) != 1:
        return -1
    else:
        sPrint("Welcome back " + rows[0][1])
        user = Agent(rows[0][0], rows[0][1], rows[0][2])

def customerLogIn(option):
    global user

    print()
    print()
    print()

    if option == 1:
        username = input("Enter a valid ID: ").strip()
        pas = getpass(prompt='Password: ')
        cursor.execute(""" SELECT * FROM customers WHERE cid=? AND pwd=?""", [username, pas])
        rows=cursor.fetchall()
        if len(rows) != 1:
            return -1
        else:
            sPrint("Welcome back " + rows[0][1])
            user = RCustomer(rows[0][0], rows[0][1], rows[0][2], rows[0][3])
    else:
        username = input("Enter a valid ID: ").strip()
        name = input("Enter your Name: ").strip()
        address = input("Enter your Address: ").strip()
        pas = getpass(prompt='Password: ')

        cursor.execute(""" SELECT * FROM customers WHERE cid=? AND pwd=?""", [username, pas])
        rows=cursor.fetchall()
        if len(rows) != 0:
            sPrint("CID and password are not unique")
            return -1
        else:
            insertions_agent = [(username, name, address, pas),]
            cursor.executemany("INSERT INTO customers VALUES (?,?,?,?)",insertions_agent);
            sPrint("Welcome " + name)
            user = RCustomer(username, name, address, pas)

def sPrint (message):
    """
    Spaced out print
    """
    print()
    print(message)
    print()

def customerMenu():
    global user
    global basket
    MENU, SEARCH, ORDER, LIST, LOGOFF = range(0,5)
    curMode = MENU
    while True:

        print()
        print()
        print()

        if curMode == MENU:
            print("CUSTOMER MENU")
            curMode = int(input("Select corresponding number: \n 1.Search\n 2.Order\n 3.List Orders\n 4.LogOff\n"))
            if curMode not in range(1,5):
                sPrint("Invalid mode. Please try again.")
                curMode=MENU
        elif curMode == SEARCH:
            #TODO: Tymoore add the search function call here

            csearch()
            curMode=MENU

        elif curMode == ORDER:
            #TODO: Add order function call here
            if len(basket) :
                placeOrder()
                basket = dict()
                print()
                if len(basket)==0:
                    print("Your basket is now empty")
                else:
                    print("Your basket is now: ", basket)
                print()
            else:
                print("Nothing to order...")
            curMode=MENU
        elif curMode == LIST:
            #TODO: Dorsa add list function
            listorder()
            curMode=MENU
        elif curMode == LOGOFF:
            logout()
            break
    sPrint("Returning to Main Menu...")


def agentMenu():
    global user
    MENU, SETUP, UPDATE, ADD, LOGOFF = range(0,5)
    curMode = MENU
    while True:
        if curMode == MENU:
            sPrint("Agent MENU")
            curMode = int(input("Select corresponding number: \n 1.Set up delivery\n 2.Update Delivery\n 3.Add to stock\n 4.LogOff\n"))
            if curMode not in range(1,5):
                sPrint("Invalid mode. Please try again.")
                curMode=MENU
        elif curMode == SETUP:
            #TODO: add the setup function call here
            setupDeliveries()
            curMode = MENU
        elif curMode == UPDATE:
            #TODO: Add update function call here
            updateDelivery()
            curMode = MENU
        elif curMode == ADD:
            #TODO:  add the add function
            addtoStock()
            # checkCarries()
            curMode = MENU
        elif curMode == LOGOFF:
            logout()
            break
    sPrint("Returning to Main Menu...")

def loginScreen():
    global user
    MENU, CUSTOMER, AGENT, QUIT = range(0,4)
    curMode = MENU
    pastMode = curMode
    while True:
        print()
        print()
        print()

        if user:
            print("Current User:", user.username)
        else:
            print("Current User: Not logged in")
        print()
        if curMode == MENU:
            print("LOG-IN SCREEN")
            curMode = int(input("Select corresponding number: \n 1.Customer \n 2.Agent \n 3.Quit Program\n"))
            if curMode not in range(1,4):
                sPrint("Please select a valid number")
                curMode = MENU
        if curMode == CUSTOMER:
            error = login(CUSTOMER)
            if error == -1:
                sPrint("Invalid ID and Password Combination. Try Again")
            elif error == -2:
                curMode = MENU
            else:
                customerMenu()
                curMode = MENU
        elif curMode == AGENT:
            error = login(AGENT)
            if error == -1:
                sPrint("Invalid ID and Password Combination. Try Again")
            elif error == -2:
                curMode = MENU
            else:
                agentMenu()
                curMode = MENU
        elif curMode == QUIT:
            logout()
            print("Exiting... ")
            break
        else:
            pass

def listorder():
    '''
    List orders. The customer should be able to see all his/her orders; the listing should include for each order, the order id, order date, the number of products ordered and the total price; the orders should be listed in a sorted order with more recent orders listed first. If there are more than 5 orders, only 5 would be shown and the user would be given an option to see more but again 5 at a time. The user should be able to select an order and see more detail of the order including delivery information such as tracking number, pick up and drop off times, the address to be delivered, and a listing of the products in the order, which will include for each product the store id, the store name, the product id, the product name, quantity, unit and unit price.
    '''
    global connection, cursor
    temp = user.username
    cursor.execute('''
    SELECT o.oid, o.odate, COUNT(ol.pid), SUM(ol.uprice)
    FROM orders o, olines ol
    WHERE o.oid = ol.oid AND o.cid=?
    GROUP BY o.oid, o.odate
    ORDER BY o.odate
     ''',[temp])
    results=cursor.fetchall()

    sPrint("")

    LAYOUT = "{!s:20} {!s:50} {!s:20} {!s:20}"

    if len(results)==0:
        print("There are no results that match.")

    elif len(results)<5:
        print(LAYOUT.format("Order ID","Order Date","Number of Products","Total Price"))
        for i in range(len(results)):
            print(LAYOUT.format(*results[i]))
        sPrint("")

        while True:
            row_index = int(input("Select the number of the row you would like to know more about (NOTE row starts at 0): "))

            if(row_index>=len(results) or row_index<0):
                print("Sorry that row does not exist please try again")
            else:
                moreInfoListOrder(results[row_index][0])
                return
        else:
            times_moved=0
        while True:
            minimum=min(times_moved*5+5,len(results))

            if(times_moved*5+5<len(results)):
                sPrint("")
                print(LAYOUT.format("Order ID","Order Date","Number of Products","Total Price"))
                for i in range(times_moved*5,minimum):
                    print(LAYOUT.format(*results[i]))
                scroll=int(input("Select 1 to see more rows or 0 to examine these rows further: "))
                if scroll==1:
                    times_moved=times_moved + 1
                    continue
                elif scroll==0:
                    pass
                else:
                    should_continue=0
                    while True:
                        print("Please select either 0 or 1")
                        scroll=int(input("Select 1 to see more rows or 0 to examine these rows further: "))
                        if scroll==0:
                            break
                        elif scroll==1:
                            times_moved=times_moved + 1
                            should_continue=1
                            break
                    if should_continue:
                        continue

            else:
                sPrint("")
                print(LAYOUT.format("Order ID","Order Date","Number of Products","Total Price"))
                for i in range(times_moved*5,len(results)):
                    print(LAYOUT.format(*results[i]))

            row_index = int(input("Select the number of the row you would like to know more about (NOTE row starts at 0): "))

            minimum=min(times_moved*5+5,len(results))
            if(row_index>=(minimum-times_moved*5) or row_index<0):
                print("Sorry that row does not exist please try again")
            else:
                moreInfoListOrder(results[times_moved*5+row_index][0])
                return


        sPrint("")


def moreInfoListOrder(oid):
    '''The user should be able to select an order and see more detail of the order including delivery information such as tracking number, pick up and drop off times, the address to be delivered, and a listing of the products in the order, which will include for each product the store id, the store name, the product id, the product name, quantity, unit and unit price.
    '''
    global cursor
    LAYOUT = "{!s:20} {!s:20} {!s:20} {!s:20}"
    print(LAYOUT.format("Tracking #","Pick up Time","Drop off Time","Address"))

    cursor.execute('''
    SELECT d.trackingNo, d.pickUpTime, d.dropOffTime,o.address
    FROM deliveries d, orders o
    WHERE d.oid = o.oid and o.oid=?
    '''
    ,[oid])

    rows1 = cursor.fetchall()
    for i in range(len(rows1)):
        print(LAYOUT.format(*rows1[i]))


    LAYOUT = "{!s:20} {!s:20} {!s:20} {!s:30} {!s:20} {!s:20} {!s:20}"
    print(LAYOUT.format("Store ID","Store Name","Product ID",'product name',"Quantity", 'Unit', 'Unit Price'))
    cursor.execute('''
    SELECT ol.sid, stores.name, ol.pid, p.name, ol.qty, p.unit, ol.uprice
    FROM products p, olines ol, stores
    WHERE p.pid = ol.pid and stores.sid = ol.sid and ol.sid = stores.sid and ol.oid = ?
    '''
    ,[oid])
    rows2 = cursor.fetchall()

    for i in range(len(rows2)):
        print(LAYOUT.format(*rows2[i]))

def main():
    setup_test() #setup()
    define_tables()
    insert_data()
    loginScreen()
    #more_info("p120")

if __name__=="__main__":
    main()








#eof
