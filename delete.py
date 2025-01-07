import mysql.connector

db = mysql.connector.connect(
    host="localhost",  
    user="root",  
    password="",
    database="customer_db"
)

cursor = db.cursor()
sql  = "DELETE FROM tabel_m_customer WHERE  customer_id=%s"
val =(3,)
cursor.execute(sql, val)

db.commit()


print("{} data dihapus".format(cursor.rowcount))