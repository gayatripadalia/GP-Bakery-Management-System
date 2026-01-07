from connection import *
from prettytable import PrettyTable
import Orders as od
import getpass as gp
def admin_login():
    global email,pw
    while True:
        email = input("Enter admin email: ")
        pw = gp.getpass("Enter password: ")
        q = 'SELECT * FROM admin WHERE e_mail=%s AND password=%s;'
        cur.execute(q, (email, pw))
        data = cur.fetchone()
        if data:
            return data[1]
        else:
            print("Invalid username or password.... Try again")
def start():
    while True:
        ch = input('''\nWelcome to GP_Bakery
1. Admin
2. Customer
3. Exit
Enter choice: ''')
        if ch == '1':
            admin_name = admin_login()
            print(f"Hello {admin_name}, Welcome to the system")
            admin_menu()
        elif ch == '2':
            customer_menu()
        elif ch == '3':
            print("Exiting system... Bye!")
            break
        else:
            print("Invalid choice")
def admin_menu():
    while True:
        ch = input('''\n***** ADMIN MENU *****
1. Category
2. Item
3. Flavours
4. Orders
5. Change Password
6. Logout
Enter choice: ''')
        if ch == '1':
            category()
        elif ch == '2':
            item()
        elif ch == '3':
            flavour()
        elif ch == '4':
            od.order_menu() 
        elif ch == '5':
            check_pass()
        elif ch == '6':
            break
        else:
            print("Invalid choice")
def customer_menu():
    while True:
        ch = input('''\n***** CUSTOMER MENU *****
1. Place New Order
2. View Items
3. View Orders
4. Go Back
Enter choice: ''')

        if ch == '1':
            od.customer_order_menu()   
        elif ch == '2':
            view_item()
        elif ch == '3':
            od.view_customer_orders()
        elif ch == '4':
            break
        else:
            print("Invalid choice")
def view_customer_orders():
    q = '''SELECT order_id, item_name, quantity, total_price, order_date
           FROM orders'''
    cur.execute(q)
    data = cur.fetchall()
    if not data:
        print("No orders found.")
        return
    t = PrettyTable(["Order ID", "Item", "Quantity", "Total Price", "Date"])
    for i in data:
        t.add_row(i)
    print(t)
def update_pass(t):
    cur.execute('UPDATE admin SET password=%s WHERE e_mail=%s', t)
    mycon.commit()
    print("Password Updated")
def check_pass():
    global pw, email
    current = input("Enter current password: ")
    if current == pw:
        new = input("Enter new password: ")
        confirm = input("Confirm password: ")
        if new == confirm:
            update_pass((confirm, email))
            pw = confirm
        else:
            print("Password mismatch")
    else:
        print("Wrong password")
def category():
    while True:
        ch = input('''\n1. Add Category
2. View Category
3. Go Back
Enter choice: ''')
        if ch == '1':
            add_category()
        elif ch == '2':
            view_category()
        elif ch == '3':
            return
        else:
            print("Invalid choice")
def check_cat_id():
    cur.execute("SELECT MAX(category_id) FROM category")
    return cur.fetchone()[0]
def add_category():
    cid = 101 if check_cat_id() is None else check_cat_id() + 1
    name = input("Enter category name: ")
    if not name.replace(" ", "").isalpha():
        print("Invalid name")
        return
    cur.execute("INSERT INTO category VALUES(%s,%s)", (cid, name))
    mycon.commit()
    print("Category Added")
def view_category():
    cur.execute("SELECT * FROM category")
    t = PrettyTable(["ID", "Name"])
    for i in cur.fetchall():
        t.add_row(i)
    print(t)
def flavour():
    while True:
        ch = input('''\n1. Add Flavour
2. View Flavour
3. Go Back
Enter choice: ''')
        if ch == '1':
            add_flavour()
        elif ch == '2':
            view_flavour()
        elif ch == '3':
            return
        else:
            print("Invalid choice")
def check_flavour_id():
    cur.execute("SELECT MAX(flav_id) FROM flavour")
    return cur.fetchone()[0]
def add_flavour():
    fid = 101 if check_flavour_id() is None else check_flavour_id() + 1
    name = input("Enter flavour name: ")
    cur.execute("INSERT INTO flavour VALUES(%s,%s)", (fid, name))
    mycon.commit()
    print("Flavour Added")
def view_flavour():
    cur.execute("SELECT * FROM flavour")
    t = PrettyTable(["ID", "Name"])
    for i in cur.fetchall():
        t.add_row(i)
    print(t)
def item():
    while True:
        ch = input('''\n1. Add Item
2. View Item
3. Go Back
Enter choice: ''')
        if ch == '1':
            add_item()
        elif ch == '2':
            view_item()
        elif ch == '3':
            return
        else:
            print("Invalid choice")
def check_item_id():
    cur.execute("SELECT MAX(item_id) FROM item_details")
    return cur.fetchone()[0]
def add_item():
    iid = 101 if check_item_id() is None else check_item_id() + 1
    name = input("Enter item name: ")
    if not name.replace(" ", "").isalpha():
        print("Invalid name")
        return
    price = int(input("Enter price: "))
    view_category()
    cat = input("Enter category id: ")
    view_flavour()
    flav = input("Enter flavour id: ")
    cur.execute("INSERT INTO item_details VALUES(%s,%s,%s,%s,%s)",
                (iid, name, price, flav, cat))
    mycon.commit()
    print("Item Added")
def view_item():
    q = '''SELECT item_id,item_name,item_price,flavour_name,category_name
           FROM item_details i
           JOIN flavour f ON i.flav_id=f.flav_id
           JOIN category c ON i.cat_id=c.category_id'''
    cur.execute(q)
    t = PrettyTable(["ID", "Name", "Price", "Flavour", "Category"])
    for i in cur.fetchall():
        t.add_row(i)
    print(t)
start()
