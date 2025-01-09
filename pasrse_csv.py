import pandas as pd
import os

def import_text_to_csv(input_file, output_file):
    """
    Import data from text file and save to CSV
    
    Parameters:
    input_file (str): Path to input text file
    output_file (str): Path to output CSV file
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
                
        # Save to CSV
        df.to_csv(output_file, 
                 index=False,  # Don't include row numbers
                 sep=',')      # Use comma as separator
        
        print(f"Data successfully imported and saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False

# Example usage
if __name__ == "__main__":
    input_file = "parse_customer.txt"
    output_file = "customer_data.csv"
    
    import_text_to_csv(input_file, output_file)