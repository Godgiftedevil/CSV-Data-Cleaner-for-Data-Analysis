import pandas as pd
import numpy as np
from datetime import datetime
import os
import glob

def detect_date_columns(df):
    """
    Detect columns that might contain date/time data
    """
    date_columns = []
    
    # First check column names for date/time indicators
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in ['date', 'time', 'datetime', 'timestamp', 'created', 'modified']):
            date_columns.append(col)
    
    # Then check data content for date patterns
    for col in df.columns:
        if col in date_columns:  # Skip if already identified
            continue
            
        # Sample non-null values to check if they look like dates
        sample_values = df[col].dropna().head(20)
        if len(sample_values) == 0:
            continue
            
        # Check for common date patterns
        date_indicators = 0
        total_sampled = 0
        
        for val in sample_values:
            if pd.isna(val) or not isinstance(val, (str, int, float)):
                continue
                
            val_str = str(val)
            total_sampled += 1
            
            # Check for common date separators and patterns
            if any(sep in val_str for sep in ['-', '/', ':', ' ']) and any(char.isdigit() for char in val_str):
                # Try to parse as date
                try:
                    pd.to_datetime(val_str)
                    date_indicators += 1
                except (ValueError, TypeError):
                    pass
        
        # If a significant portion of sampled values look like dates
        if total_sampled > 0 and date_indicators / total_sampled > 0.3:
            date_columns.append(col)
    
    return date_columns

def convert_to_datetime(df, date_columns):
    """
    Convert detected date columns to datetime format
    """
    df_converted = df.copy()
    
    for col in date_columns:
        if col not in df_converted.columns:
            continue
            
        # Try different approaches to convert to datetime
        try:
            # First try pandas to_datetime with errors='coerce'
            df_converted[col] = pd.to_datetime(df_converted[col], errors='coerce', infer_datetime_format=True)
        except Exception as e:
            print(f"Warning: Could not convert column '{col}' to datetime: {e}")
    
    return df_converted

def clean_dataframe(df, exclude_columns=[]):
    """
    Comprehensive data cleaning function
    """
    print("Starting data cleaning process...")
    
    # Create a copy to avoid modifying the original dataframe
    df_cleaned = df.copy()
    
    # Initial info
    initial_rows, initial_cols = df_cleaned.shape
    print(f"Initial data shape: {initial_rows} rows, {initial_cols} columns")
    
    # Detect and convert date/time columns
    date_columns = detect_date_columns(df_cleaned)
    print(f"Detected date/time columns: {date_columns}")
    df_cleaned = convert_to_datetime(df_cleaned, date_columns)
    
    # Handle text columns
    text_columns = df_cleaned.select_dtypes(include='object').columns
    print(f"Text columns to clean: {list(text_columns)}")
    
    for col in text_columns:
        if col not in exclude_columns:
            # Convert to string and clean
            df_cleaned[col] = df_cleaned[col].astype(str)
            
            # Strip whitespace
            df_cleaned[col] = df_cleaned[col].str.strip()
            
            # Only convert to lowercase if it's not a date column
            if col not in date_columns:
                df_cleaned[col] = df_cleaned[col].str.lower()
            
            # Replace 'nan' strings with actual NaN values
            df_cleaned[col] = df_cleaned[col].replace('nan', np.nan)
            
            # Replace 'none' strings with actual NaN values
            df_cleaned[col] = df_cleaned[col].replace('none', np.nan)
    
    # Remove rows with all NaN values
    df_cleaned = df_cleaned.dropna(how='all')
    all_nan_removed = initial_rows - len(df_cleaned)
    if all_nan_removed > 0:
        print(f"Removed {all_nan_removed} rows with all NaN values")
    
    # Remove duplicate rows
    initial_rows_after_nan = len(df_cleaned)
    df_cleaned = df_cleaned.drop_duplicates()
    duplicates_removed = initial_rows_after_nan - len(df_cleaned)
    if duplicates_removed > 0:
        print(f"Removed {duplicates_removed} duplicate rows")
    
    # Reset index
    df_cleaned = df_cleaned.reset_index(drop=True)
    
    # Final info
    final_rows, final_cols = df_cleaned.shape
    print(f"Final data shape: {final_rows} rows, {final_cols} columns")
    print(f"Total rows removed: {initial_rows - final_rows}")
    
    return df_cleaned

def list_csv_files():
    """
    List all CSV files in the current directory
    """
    csv_files = glob.glob("*.csv")
    return csv_files

def select_file_interactive():
    """
    Interactive file selection
    """
    csv_files = list_csv_files()
    
    if not csv_files:
        print("No CSV files found in the current directory.")
        print("Please upload your CSV file to: c:/Users/dell/Documents/data")
        return None
    
    print("\nAvailable CSV files:")
    for i, file in enumerate(csv_files, 1):
        print(f"{i}. {file}")
    
    try:
        choice = int(input(f"\nEnter the number of the file you want to clean (1-{len(csv_files)}): "))
        if 1 <= choice <= len(csv_files):
            return csv_files[choice-1]
        else:
            print("Invalid choice.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

def save_cleaned_data(df, original_filename):
    """
    Save the cleaned dataframe to a CSV file
    """
    # Generate output filename
    base_name = original_filename.rsplit('.', 1)[0]
    output_filename = f"{base_name}_cleaned.csv"
    
    df.to_csv(output_filename, index=False)
    print(f"\nCleaned data saved to: {output_filename}")
    print("You can find this file in the same directory.")
    return output_filename

def process_csv_file(file_path, exclude_columns=[]):
    """
    Main function to process a CSV file
    """
    try:
        # Read the CSV file
        print(f"Reading file: {file_path}")
        df = pd.read_csv(file_path, low_memory=False)
        print(f"Original data shape: {df.shape}")
        
        # Clean the dataframe
        print("\nCleaning data...")
        df_cleaned = clean_dataframe(df, exclude_columns)
        
        # Save cleaned data
        output_file = save_cleaned_data(df_cleaned, os.path.basename(file_path))
        
        return df_cleaned, output_file
        
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None, None

def main():
    """
    Main interactive function
    """
    print("=" * 50)
    print("CSV DATA CLEANING TOOL")
    print("=" * 50)
    print("Place your CSV file in the folder: c:/Users/dell/Documents/data")
    print("This script will automatically detect and clean your data.\n")
    
    # Get file to process
    file_path = select_file_interactive()
    
    if file_path is None:
        return
    
    # Process the file
    print(f"\nProcessing file: {file_path}")
    cleaned_df, output_file = process_csv_file(file_path)
    
    if cleaned_df is not None:
        print("\nData cleaning completed successfully!")
        print(f"Cleaned file saved as: {output_file}")
        print("\nSummary of changes:")
        print(f"- Columns standardized")
        print(f"- Date/time formats corrected")
        print(f"- Text data normalized")
        print(f"- Empty rows removed")
        print(f"- Duplicate rows removed")
        print("\nThe cleaned file is ready to use!")

if __name__ == "__main__":
    main()
