import mysql.connector

db = mysql.connector.connect(
    host="localhost",  
    user="root",  
    password="",
    database="customer_db"
)

if db.is_connected():
  print("Berhasil terhubung ke database")


