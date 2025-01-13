"""
Script untuk mengimpor data dari database MySQL ke file Excel.

- Menggunakan koneksi ke database MySQL dengan konfigurasi yang diberikan.
- Mengeksekusi query SQL untuk mengambil data dari tabel database.
- Menyimpan data yang diambil ke file Excel di folder output yang ditentukan.
- Menyediakan logging untuk mencatat semua aktivitas, seperti eksekusi query, jumlah data yang diambil, dan status proses.
"""

import pandas as pd
import mysql.connector
import os
from datetime import datetime
from config import setup_logger 

logger = setup_logger(log_folder="logs", log_filename="importDb_excel")

def export_db_to_excel(db_config, query, output_folder):
    try:
        logger.info("Memulai proses Import data dari database ke Excel.")
        logger.info(f"Query yang dieksekusi: {query}")
        
        db = mysql.connector.connect(**db_config)
        df = pd.read_sql(query, db)
        logger.info(f"Query berhasil dieksekusi. Jumlah data: {len(df)} baris, {len(df.columns)} kolom.")
        
        if not df.empty:
            logger.info(df.head(5).to_string(index=False))
        else:
            logger.warning("Data yang diimpor kosong.")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_folder, f"customer_data_{timestamp}.xlsx")
        
        df.to_excel(output_file, sheet_name='Customer Data', index=False)
        logger.info(f"Data berhasil Di Import ke file {output_file}.")
        
        db.close()
        return True
    
    except Exception as e:
        logger.error(f"Terjadi error selama proses ekspor: {str(e)}")
        return False

if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "customer_db"
    }
    
    query = "SELECT customer_id, customer_name, email, phone_number, created_at FROM tabel_m_customer"
    output_folder = r"C:\PythonProjects\selesai_import"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logger.info(f"Folder output {output_folder} dibuat.")
        
    success = export_db_to_excel(db_config, query, output_folder)
    if success:
        logger.info("Proses Import Sukses.")
    else:
        logger.error("Proses Import Gagal.")
