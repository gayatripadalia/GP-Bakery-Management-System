from connection import *
from prettytable import PrettyTable
import datetime as dt
today = dt.datetime.today()
cart = {}
def order_menu():
    while True:
        ch = input('''\n***** ORDER MENU (ADMIN) *****
1. New Order
2. View All Orders
3. Go Back
Enter choice: ''')
        if ch == '1':
            new_order()
        elif ch == '2':
            view_all_orders()
        elif ch == '3':
            break
        else:
            print("Invalid choice")
def customer_order_menu():
    while True:
        ch = input('''\n***** PLACE ORDER *****
1. New Order
2. Go Back
Enter choice: ''')

        if ch == '1':
            new_order()
        elif ch == '2':
            break
        else:
            print("Invalid choice")
def new_order():
    global cart, order_id
    cart = {}
    order_id = get_max_order_id() + 1
    while True:
        view_item()
        item_id = get_valid_item_id()
        qty = get_quantity()
        cart[item_id] = cart.get(item_id, 0) + qty
        show_order_info()
        ch = input("Add more items? (1 = Yes / Any key = No): ")
        if ch != '1':
            break
    print("\nTotal Amount =", grand_total)
    save_order()
def get_max_order_id():
    cur.execute("SELECT MAX(ord_id) FROM order1;")
    x = cur.fetchone()[0]
    return 0 if x is None else x
def get_valid_item_id():
    while True:
        item_id = input("Enter item id: ")
        cur.execute("SELECT item_id FROM item_details WHERE item_id=%s;", (item_id,))
        if cur.fetchone():
            return int(item_id)
        else:
            print("Invalid item id")
def get_quantity():
    while True:
        q = input("Enter quantity: ")
        if q.isdigit() and int(q) > 0:
            return int(q)
        print("Invalid quantity")
def get_item_info(item_id):
    q = '''SELECT i.item_name, i.item_price,
                  f.flavour_name, c.category_name
           FROM item_details i
           JOIN flavour f ON i.flav_id=f.flav_id
           JOIN category c ON i.cat_id=c.category_id
           WHERE i.item_id=%s'''
    cur.execute(q, (item_id,))
    return cur.fetchone()
def show_order_info():
    global grand_total
    grand_total = 0
    table = PrettyTable(['S.N.', 'Item', 'Price', 'Qty', 'Total'])
    sn = 1
    for item_id, qty in cart.items():
        data = get_item_info(item_id)
        name = f"{data[0]} {data[2]} {data[3]}"
        total = data[1] * qty
        grand_total += total
        table.add_row([sn, name, data[1], qty, total])
        sn += 1
    print(table)
def save_order():
    cname = input("Enter customer name: ")
    cadd = input("Enter address: ")
    ccontact = input("Enter contact number: ")

    for item_id, qty in cart.items():
        q = '''INSERT INTO order1
               (ord_id, item_id, order_date, quantity,
                customer_name, customer_address, customer_contact)
               VALUES (%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(q, (order_id, item_id, today, qty,
                        cname, cadd, ccontact))
    mycon.commit()
    print("\nOrder placed successfully!")
def view_all_orders():
    q = '''SELECT ord_id, order_date, customer_name,
                  customer_contact, item_id, quantity
           FROM order1
           ORDER BY ord_id'''
    cur.execute(q)
    data = cur.fetchall()
    if not data:
        print("No orders found.")
        return
    table = PrettyTable(
        ['Order ID', 'Date', 'Customer', 'Contact', 'Item ID', 'Qty']
    )
    for i in data:
        table.add_row(i)
    print(table)
def view_customer_orders():
    q = '''SELECT o.ord_id, i.item_name,
                  o.quantity,
                  (o.quantity * i.item_price) AS total
           FROM order1 o
           JOIN item_details i ON o.item_id=i.item_id'''
    cur.execute(q)
    data = cur.fetchall()
    if not data:
        print("No orders found.")
        return
    table = PrettyTable(['Order ID', 'Item', 'Qty', 'Total'])
    for i in data:
        table.add_row(i)
    print(table)
def view_item():
    q = '''SELECT i.item_id, i.item_name, i.item_price,
                  f.flavour_name, c.category_name
           FROM item_details i
           JOIN flavour f ON i.flav_id=f.flav_id
           JOIN category c ON i.cat_id=c.category_id'''
    cur.execute(q)
    data = cur.fetchall()
    if not data:
        print("No items available.")
        return
    table = PrettyTable(['Item ID', 'Item Name', 'Price', 'Flavour', 'Category'])
    for i in data:
        table.add_row(i)
    print(table)
