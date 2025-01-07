import mysql.connector

db = mysql.connector.connect(
    host="localhost",  
    user="root",  
    password="",
    database="customer_db"
)


cursor = db.cursor()
sql = "INSERT INTO tabel_m_customer (customer_name, email, phone_number) VALUES (%s, %s, %s)"
values = [
  ("Helmi Tazkia", "helmitazkia85gmail.com", "085723423"),
  ("Hardi Rama", "hardi@gmail.com","08765235734")
]

for val in values:
  cursor.execute(sql, val)
  db.commit()

print("{} data ditambahkan".format(len(values)))

