import sqlite3
from getpass import getpass

connection = None
cursor = None

def setup():
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
    # TODO: Insert appropriate data THAT FOLLOWS FOREIGN KEY RESTRAINTS!!!!
    # Dorsa, make data :)
    global connection, cursor
    insertions_cat = [('bak','Bakery'),
    ('pro','Produce'),
    ('ele','Electronics'),
    ('clo','ClothingandApparel'),
    ('hom','HomeAppliances'),
    ('toy','Childrenssection'),
    ('kid','KidsClothingandApparel'),
    ('car','Autoshops'),]
    cursor.executemany("INSERT INTO categories VALUES (?,?)",insertions_cat);


    insertions_products = [('p10','4Lmilk1%','ea','dai'),
    ('p20','dozenlargeegg','ea','dai'),
    ('p30','cheddarcheese(270g)','ea','dai'),
    ('p40','whiteslicedbread','ea','bak'),
    ('p50','dozendonuts','ea','bak'),
    ('p60','reddeliciousapple','lb','pro'),
    ('p70','galaapple','lb','pro'),
    ('p80','babycarrots(454g)','ea','pro'),
    ('p90','broccoli','lb','pro'),
    ('p100','headphones','ea','ele'),
    ('p110','8gbsdhcCard','ea','ele'),
    ('p120','aaabatteries(8-pk)','ea','ele'),
    ('p130','ledhdtv,32-in','ea','ele'),
    ('p140','v-necksweater','ea','clo'),
    ('p150','cottonhoodie','ea','clo'),
    ('p160','coffeemaker','ea','hom'),
    ('p170','toaster','ea','hom'),
    ('p180','foodmixer','ea','hom'),]
    cursor.executemany("INSERT INTO products VALUES	(?, ?, ?, ?)",	insertions_products);

    # customers(cid, name, address, pwd)
    insertions_cust = [('1','Bob', '12345 Ave', 'ezpass'),
    ('2', 'Joe', '13 Street', 'pass'),]
    cursor.executemany("INSERT INTO customers VALUES (?,?,?,?)",insertions_cust);

    # agents(aid, name, pwd)
    insertions_agent = [('12','James Bond', '007'),
    ('23', 'Joe Smith', '23'),]
    cursor.executemany("INSERT INTO agents VALUES (?,?,?)",insertions_agent);

def search_for_keyword(keywords):
    global connection, cursor
    keyword_list=keywords.split(" ")
    results=[]
    for key in keyword_list:
        k="%"+key+"%"
        cursor.execute("SELECT * FROM products p WHERE p.name LIKE ? ",[k])
        rows=cursor.fetchall()
        results=results+rows
    return results

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

def login(userType): #cid, name, address, pwd)
    if userType == 1:
        option = input("Select corresponding number: \n1.Log In \n2.Sign Up \n")
        customerLogIn(option)
    else :  # AGENT Menu
        agentLogin()

def agentLogin():
    username = input("Enter a valid ID: ").strip()
    pas = getpass(prompt='Password: ')
    cursor.execute(""" SELECT * FROM agents WHERE aid=? AND pwd=?""", [username, pas])
    rows=cursor.fetchall()
    if len(rows) != 1:
        return -1
    else:
        sPrint("Welcome back" + rows[0][1])
        return Agent(rows[0][0], rows[0][1], rows[0][2])

def customerLogIn(option):
    if option == 1:
        username = input("Enter a valid ID: ").strip()
        pas = getpass(prompt='Password: ')
        cursor.execute(""" SELECT * FROM customers WHERE cid=? AND pwd=?""", [username, pas])
        rows=cursor.fetchall()
        if len(rows) != 1:
            return -1
        else:
            sPrint("Welcome back " + rows[0][1])
            return RCustomer(rows[0][0], rows[0][1], rows[0][2], rows[0][3])
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
            return RCustomer(username, name, address, pas)

def sPrint (message):
    print()
    print(message)
    print()

def main():
    setup()
    define_tables()
    insert_data()
    print(search_for_keyword('oo tt'))

    search_for_keyword('hello goodbye')
    MENU, CUSTOMER, AGENT, LOGOFF, QUIT = range(0,5)
    curMode = MENU
    pastMode = curMode
    user = None
    while True:
        if curMode == MENU:
            print("LOG-IN SCREEN")
            curMode = int(input("Select corresponding number: \n 1.Customer \n 2.Agent \n 3.LogOff \n 4.Quit Program\n "))
        if curMode == CUSTOMER:
            #TODO: Implement the Customer and Agent menus
            user = login(CUSTOMER)
            if user == -1:
                sPrint("Invalid ID and Password Combination. Try Again")
            else:
                curMode = MENU
        elif curMode == AGENT:
            user = login(AGENT)
            if user == -1:
                sPrint("Invalid ID and Password Combination. Try Again")
            else:
                curMode = MENU
        elif curMode == LOGOFF:
            user = None
            sPrint("Logging out...")
            curMode = MENU
        else:
            print("Exiting... ")
            break


if __name__=="__main__":
    main()








#eof
