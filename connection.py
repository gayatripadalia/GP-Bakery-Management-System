import mysql.connector as msql
from prettytable import PrettyTable
mycon = msql.connect(
    host="localhost",
    user="root",
    password="YourPassword",  # replace with your MySQL password
    database="GP_bakery"
)
cur = mycon.cursor()
