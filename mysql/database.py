import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="my-secret-pw",
  database="my_database"
)

mycursor = mydb.cursor()

sql = "INSERT INTO my_table (usuario, mensagem) VALUES (%s, %s)"
val = ("John", "Hello World")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")