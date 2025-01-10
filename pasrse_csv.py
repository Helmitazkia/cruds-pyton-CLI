"""
Kode ini digunakan untuk mengimpor data dari file teks ke dalam file CSV. 
File teks akan diproses, diformat, dan disimpan dengan nama file CSV yang mencakup timestamp.
"""

import pandas as pd
import os
from datetime import datetime

def import_text_to_csv(input_file, output_file):
    """
    Import data from text file and save to CSV with a timestamped filename.
    
    Parameters:
    input_file (str): Path to input text file
    output_file (str): Base name for output CSV file (without timestamp).
    """
    try:
        df = pd.read_csv(input_file, 
                         delimiter='\t',
                         names=['customer_id', 'customer_name', 'email', 
                                'phone_number', 'created_at'])
        
        for column in df.columns:
            if df[column].dtype == 'object':
                df[column] = df[column].str.strip()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{os.path.splitext(output_file)[0]}_{timestamp}.csv"
        
        df.to_csv(output_file, 
                  index=False,
                  sep=',')
        
        
        print(f"Data successfully imported and saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    input_file = r"C:\PythonProjects\selesai_convert\convert_customer.txt"
    output_file = r"C:\PythonProjects\selesai_import\convert_customer.csv"
    
    import_text_to_csv(input_file, output_file)
