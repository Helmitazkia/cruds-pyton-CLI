import mysql.connector
import os

def process_line(line):
    """
    Memproses satu baris teks untuk memisahkan nama, email, dan nomor telepon.
    """
    parts = line.split()
    if len(parts) < 3:
        return None  # Baris tidak valid
    name = " ".join(parts[:-2])
    email = parts[-2]
    phone = parts[-1]
    return name, email, phone

def import_text_to_db(txt_file, db_config):
    """
    Parse file teks dan masukkan data ke database MySQL.
    
    Parameter:
    txt_file (str): Path atau lokasi file teks input.
    db_config (dict): Konfigurasi untuk koneksi database.
    """
    try:
        data = []

        with open(txt_file, 'r') as file:
            for line in file:
                processed = process_line(line.strip())
                if processed:
                    data.append(processed)

        if not data:
            print(f"File {txt_file} tidak mengandung data yang valid.")
            return False

        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        sql = """INSERT INTO tabel_m_customer 
                 (customer_name, email, phone_number) 
                 VALUES (%s, %s, %s)"""

        cursor.executemany(sql, data)
        db.commit()

        print(f"{cursor.rowcount} rows successfully inserted from {txt_file}")

        cursor.close()
        db.close()

        return True

    except FileNotFoundError:
        print(f"Error: File '{txt_file}' tidak ditemukan.")
        return False
    except mysql.connector.Error as db_error:
        print(f"Database error: {db_error}")
        if 'db' in locals():
            db.close()
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        if 'db' in locals():
            db.close()
        return False

if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "customer_db"
    }
    
    folder_path = r"C:\PythonProjects\selesai_convert"

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            result = import_text_to_db(file_path, db_config)
            if result:
                print(f"Import berhasil untuk file: {file_path}")
                os.remove(file_path)
                print(f"File {file_name} telah dihapus.")
            else:
                print(f"Import gagal untuk file: {file_path}")
