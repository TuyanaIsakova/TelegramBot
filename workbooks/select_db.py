import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="17022009Mysql"
)

mycursor = mydb.cursor()

mycursor.execute("""
    SELECT *
    FROM   product.transactions
    """)

myresult = mycursor.fetchall()

for x in myresult:
  print(x)