import mysql.connector

db = mysql.connector.connect(
    host="localhost",  
    user="root",  
    password="",
    database="customer_db"
)


cursor = db.cursor()
sql = "UPDATE tabel_m_customer SET customer_name=%s, email=%s, phone_number=%s WHERE customer_id=%s"
val = ("Helmi", "helmitazkia85.com", "08572342321" , 3)
cursor.execute(sql, val)

db.commit()

print("{} data diubah".format(cursor.rowcount))

