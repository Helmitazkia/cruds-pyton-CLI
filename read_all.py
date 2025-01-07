import mysql.connector

db = mysql.connector.connect(
    host="localhost",  
    user="root",  
    password="",
    database="customer_db"
)


cursor = db.cursor()
sql = "SELECT * FROM tabel_m_customer"
cursor.execute(sql)

results = cursor.fetchall()

for data in results:
  print(data)