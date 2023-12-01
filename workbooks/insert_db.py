import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="17022009Mysql"
)

mycursor = mydb.cursor()

sql = """
    INSERT INTO product.transactions (
        name,
        dt,
        money,
        reason
        ) 
    VALUES (%s, %s, %s, %s)
    """
val = ("John", "2023-12-01 00:00:09.3443434", 200, 'hotel')
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")