import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="17022009Mysql"
)

mycursor = mydb.cursor()

mycursor.execute("""
    SELECT name,
           sum(money) as total
    FROM   product.transactions
    GROUP BY name
    """)

myresult = mycursor.fetchall()

for x in myresult:
  print(x)