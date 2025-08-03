# CSV Data Cleaning Tool

This tool automatically cleans CSV files by:
- Detecting and properly formatting date/time columns
- Normalizing text data (removing extra whitespace, converting to lowercase)
- Removing empty rows and duplicates
- Handling missing values appropriately

## How to Use This Tool

1. **Place your CSV file** in the folder: `c:/Users/dell/Documents/data`
2. **Run the script** by double-clicking on `csv_data_cleaner.py` or running it from the command line:
   ```
   python csv_data_cleaner.py
   ```
3. **Follow the prompts** to select which file you want to clean
4. **Find your cleaned file** with "_cleaned" appended to the original filename

## Features

- **Automatic Date Detection**: The tool automatically identifies columns that contain date/time information
- **Date Format Standardization**: Converts various date formats to a consistent datetime format
- **Text Normalization**: Removes extra whitespace and standardizes text case
- **Data Deduplication**: Removes duplicate rows from your dataset
- **Missing Value Handling**: Properly handles empty cells and NaN values
- **Interactive File Selection**: Easy-to-use interface for selecting files to clean

## Requirements

- Python 3.x
- pandas
- numpy

## Output

The cleaned CSV file will be saved in the same directory with "_cleaned" appended to the original filename.
For example: `data.csv` becomes `data_cleaned.csv`

## Support

For any issues or questions, please contact the author at [sauravggd@gmail.com] or [Godgiftedevil].
