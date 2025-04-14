import sqlite3
import pandas as pd
import os
from pathlib import Path

def sqlite_to_csv(db_file, output_dir='csv_output'):
    """
    Convert all tables in a SQLite database to CSV files.
    
    Parameters:
    - db_file: Path to the SQLite .db file
    - output_dir: Directory where CSV files will be saved
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Get list of all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("No tables found in the database.")
            return
        
        # Loop through each table and export to CSV
        for table_name in tables:
            table_name = table_name[0]
            print(f"Exporting table: {table_name}")
            
            try:
                # Read table into pandas DataFrame
                query = f"SELECT * FROM {table_name}"
                df = pd.read_sql_query(query, conn)
                
                # Generate CSV file path
                csv_file = os.path.join(output_dir, f"{table_name}.csv")
                
                # Save DataFrame to CSV
                df.to_csv(csv_file, index=False, encoding='utf-8')
                print(f"Successfully saved {table_name} to {csv_file}")
                
            except Exception as e:
                print(f"Error exporting table {table_name}: {str(e)}")
        
        # Close the connection
        conn.close()
        print("Conversion completed.")
        
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")

if __name__ == "__main__":
    data_dir = Path(__file__).parent / "data"
    db_file = data_dir / "game_content.db"
    csv_file = data_dir
    
    sqlite_to_csv(db_file, csv_file)