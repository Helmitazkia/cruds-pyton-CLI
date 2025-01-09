import mysql.connector
import pandas as pd
import numpy as np

def import_text_to_db(txt_file, db_config):
    """
    Parse file teks dan masukkan data ke database MySQL.
    
    Parameter:
    txt_file (str): Path atau lokasi file teks input.
    db_config (dict): Konfigurasi untuk koneksi database.
    """
    try:
     
        df = pd.read_csv(
            txt_file, 
            delimiter=',',  
            names=['customer_name', 'email', 'phone_number'],  
            na_filter=True,  
            dtype=str  
        )

        df = df.replace({np.nan: None})

     
        for column in df.columns:
            if df[column].dtype == 'object': 
                df[column] = df[column].apply(lambda x: x.strip() if x else x)

      
        print("Debugging DataFrame:")
        print(df)

        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

    
        sql = """INSERT INTO tabel_m_customer 
                 (customer_name, email, phone_number) 
                 VALUES (%s, %s, %s)"""

       
        values = df.values.tolist()

    
        cursor.executemany(sql, values)

       
        db.commit()

      
        print(f"{cursor.rowcount} rows successfully inserted into the database.")

        # Menutup koneksi database
        cursor.close()
        db.close()

        return True

    # Penanganan error jika file tidak ditemukan
    except FileNotFoundError:
        print(f"Error: File '{txt_file}' tidak ditemukan.")
        return False
    # Penanganan error jika terjadi kesalahan pada database
    except mysql.connector.Error as db_error:
        print(f"Database error: {db_error}")
        if 'db' in locals():
            db.close()
        return False
    # Penanganan error umum lainnya
    except Exception as e:
        print(f"Error: {str(e)}")
        if 'db' in locals():
            db.close()
        return False

# Contoh penggunaan
if __name__ == "__main__":
    # Konfigurasi database
    db_config = {
        "host": "localhost",  # Host atau alamat server database
        "user": "root",  # Username untuk login ke database
        "password": "",  # Password untuk login
        "database": "customer_db"  # Nama database yang akan digunakan
    }
    
    # File input
    input_file = "customer_import.txt"  # Lokasi file teks input
    
    # Jalankan fungsi untuk mengimpor data dari file teks ke database
    result = import_text_to_db(input_file, db_config)
    if result:
        print("Data import berhasil dilakukan.")
    else:
        print("Data import gagal.")
