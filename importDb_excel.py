import pandas as pd
import mysql.connector
import os
from datetime import datetime

def export_db_to_excel(db_config, query, output_folder):
    try:
        db = mysql.connector.connect(**db_config)
        df = pd.read_sql(query, db)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_folder, f"customer_data_{timestamp}.xlsx")
        df.to_excel(output_file, sheet_name='Customer Data', index=False)
        print(f"Data successfully exported to {output_file}")
        db.close()
        return True
    except Exception as e:
        print(f"Error occurred: {str(e)}")
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
    
    export_db_to_excel(db_config, query, output_folder)
