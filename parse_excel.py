import pandas as pd
import os

def import_text_to_excel(input_file, output_file):
    """
    Import data from text file and save to Excel
    
    Parameters:
    input_file (str): Path to input text file
    output_file (str): Path to output Excel file
    """
    try:
        # Read the text file with proper column names
        df = pd.read_csv(input_file, 
                        delimiter='\t',  # Using tab as delimiter
                        names=['customer_id', 'customer_name', 'email', 
                              'phone_number', 'created_at'])
        
        # Clean the data (remove any extra whitespace)
        for column in df.columns:
            if df[column].dtype == 'object':  # Only clean string columns
                df[column] = df[column].str.strip()
                
        # Save to Excel
        df.to_excel(output_file, 
                   sheet_name='Customer Data',
                   index=False)  # Don't include row numbers
        
        print(f"Data successfully imported and saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False

# Example usage
if __name__ == "__main__":
    input_file = "tabel_m_customer.txt"
    output_file = "customer_data.xlsx"
    
    import_text_to_excel(input_file, output_file)