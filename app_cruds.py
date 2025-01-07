import mysql.connector
import os

db = mysql.connector.connect(
    host="localhost",  
    user="root",  
    password="",
    database="customer_db"
)

def insert_data(db):
  name = input("Masukan nama: ")
  email = input("Masukan Email: ")
  phone_number = input("Masukan Nomor Handphone: ")
  val = (name, email,phone_number)
  cursor = db.cursor()
  sql = "INSERT INTO tabel_m_customer (customer_name, email, phone_number) VALUES (%s, %s, %s)"
  cursor.execute(sql, val)
  db.commit()
  print("{} data berhasil disimpan".format(cursor.rowcount))


def show_data(db):
  cursor = db.cursor()
  sql = "SELECT * FROM tabel_m_customer"
  cursor.execute(sql)
  results = cursor.fetchall()
  
  if cursor.rowcount < 0:
    print("Tidak ada data")
  else:
    for data in results:
      print(data)


def update_data(db):
  cursor = db.cursor()
  show_data(db)
  customer_id = input("pilih id customer> ")
  name = input("Nama baru: ")
  email = input("Email Baru: ")
  phone_number = input("Nomor Handphone Baru: ")
  sql = "UPDATE tabel_m_customer SET customer_name=%s, email=%s, phone_number=%s WHERE customer_id=%s"
  val = (name, email,phone_number, customer_id)
  cursor.execute(sql, val)
  db.commit()
  print("{} data berhasil diubah".format(cursor.rowcount))


def delete_data(db):
  cursor = db.cursor()
  show_data(db)
  customer_id = input("pilih id customer> ")
  sql = "DELETE FROM tabel_m_customer WHERE customer_id=%s"
  val = (customer_id,)
  cursor.execute(sql, val)
  db.commit()
  print("{} data berhasil dihapus".format(cursor.rowcount))





def show_menu(db):
  print("=== APLIKASI DATABASE PYTHON ===")
  print("1. Insert Data")
  print("2. Tampilkan Data")
  print("3. Update Data")
  print("4. Hapus Data")
  print("0. Keluar")
  print("------------------")
  menu = input("Pilih menu> ")

  #clear screen
  os.system("clear")

  if menu == "1":
    insert_data(db)
  elif menu == "2":
    show_data(db)
  elif menu == "3":
    update_data(db)
  elif menu == "4":
    delete_data(db)
  elif menu == "0":
    exit()
  else:
    print("Menu salah!")


if __name__ == "__main__":
  while(True):
    show_menu(db)