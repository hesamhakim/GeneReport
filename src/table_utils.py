"""
Utilities for extracting tables from PDF files using Camelot.
"""

import camelot
import os
import pandas as pd

def extract_tables_from_pdf(pdf_dir, pdf_file, output_folder, pages="all", flavor='lattice', line_scale=60):
    """
    Extract tables from a PDF file using Camelot and save them as CSV files.
    
    Args:
        pdf_dir (str): Directory containing PDF files
        pdf_file (str): Name of the PDF file
        output_folder (str): Directory to save extracted tables
        pages (str): Pages to extract tables from, default is "all"
        flavor (str): Camelot extraction method ('lattice' or 'stream')
        line_scale (int): Line scale parameter for Camelot
        
    Returns:
        bool: True if tables were extracted and saved, False otherwise
    """
    # Using lattice mode as an example, which works well for PDFs with clear table borders
    tables = camelot.read_pdf(
        os.path.join(pdf_dir, pdf_file), 
        pages=pages, 
        flavor=flavor, 
        line_scale=line_scale
    )
    report_name = os.path.splitext(pdf_file)[0]

    # Check if any tables are found
    if tables.n == 0:
        print(f"No table from '{pdf_file}' saved")
        return False  # Return False if no tables found
    
    # Iterate over found tables and save them as CSV
    for i, table in enumerate(tables, start=1):
        # Save the table as a CSV
        csv_file = f"{report_name}_table_camelot_{i}.csv"
        csv_path = os.path.join(output_folder, csv_file)
        table.to_csv(csv_path)
        print(f"Table {i} from '{pdf_file}' saved as '{csv_file}'")
    
    return True  # Return True if tables were found

def process_pdf_directory(pdf_dir, output_folder):
    """
    Process all PDFs in a directory and extract tables.
    
    Args:
        pdf_dir (str): Directory containing PDF files
        output_folder (str): Directory to save extracted tables
        
    Returns:
        list: List of PDF filenames with no tables found
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Track PDFs with no tables
    no_tables_pdfs = []
    
    # Process all PDFs
    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            has_tables = extract_tables_from_pdf(pdf_dir, pdf_file, output_folder)
            if not has_tables:
                no_tables_pdfs.append(pdf_file)
    
    return no_tables_pdfs

def save_pdfs_without_tables(no_tables_pdfs, output_folder):
    """
    Save list of PDFs with no tables to a CSV file.
    
    Args:
        no_tables_pdfs (list): List of PDF filenames
        output_folder (str): Directory to save the CSV file
        
    Returns:
        str: Path to the saved CSV file
    """
    # Create DataFrame of PDFs with no tables
    no_tables_df = pd.DataFrame(no_tables_pdfs, columns=['PDF_Filename'])
    
    # Save the DataFrame to CSV
    no_tables_csv_path = os.path.join(output_folder, 'pdfs_with_no_tables.csv')
    no_tables_df.to_csv(no_tables_csv_path, index=False)
    
    return no_tables_csv_path