"""
Utilities for processing PDF files, specifically for extracting and splitting
OncoKids pathology reports from larger PDF files.
"""

import re
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter

def search_specimen_in_pdf(pdf_file, pattern):
    """
    Find all specimen IDs based on pattern and associate them with page number.
    
    Args:
        pdf_file (str): Path to the PDF file
        pattern (str): Regex pattern to match specimen IDs
    
    Returns:
        list: List of dictionaries containing match results and page numbers
    """
    results = []
    with open(pdf_file, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
        
        for page_number, page in enumerate(pdf_reader.pages, 1):
            text = page.extract_text()
            matches = re.finditer(pattern, text)
            for match in matches:
                results.append({'Result': match.group(), 'Page': page_number})
                
    return results

def generate_table(results):
    """
    Convert search results to a pandas DataFrame.
    
    Args:
        results (list): List of dictionaries with search results
    
    Returns:
        pandas.DataFrame: DataFrame containing the search results
    """
    df = pd.DataFrame(results)
    return df

def print_unique_values(df):
    """
    Print the count of unique values in each column of a DataFrame.
    
    Args:
        df (pandas.DataFrame): DataFrame to analyze
    """
    for column in df.columns:
        unique_count = df[column].nunique()
        print(f"Unique values in Column '{column}' = {unique_count}")

def find_pages_btw_keywords(pdf_file, regex1, regex2, max_dist):
    """
    Find pages between two given regex patterns.
    Used to extract oncokids reports for each specimen ID.
    
    Args:
        pdf_file (str): Path to the PDF file
        regex1 (str): First regex pattern to match
        regex2 (str): Second regex pattern to match
        max_dist (int): Maximum page distance to search for second pattern
        
    Returns:
        list: List of dictionaries with start and end page numbers
    """
    reader = PdfReader(pdf_file)
    num_pages = len(reader.pages)
    results = []
    
    current_page = 0
    while current_page < num_pages:
        start_page_number = None
        
        # Loop until we find a match for regex1
        while current_page < num_pages:
            page_text = reader.pages[current_page].extract_text()
            if re.search(regex1, page_text):
                start_page_number = current_page + 1
                break
            current_page += 1
        
        if start_page_number is None:
            break  # No more matches for regex1, end search
        
        # Search for regex2 within the next max_dist pages
        end_page_number = None
        for i in range(current_page + 1, min(current_page + 1 + max_dist, num_pages)):
            next_page_text = reader.pages[i].extract_text()
            if re.search(regex2, next_page_text):
                end_page_number = i + 1
                current_page = i + 1  # Move to the page after the match
                break
        
        if end_page_number:
            results.append({"start_page_number": start_page_number, "end_page_number": end_page_number})
        else:
            current_page += 1  # Continue searching from the next page after the match of regex1

    return results

def extract_pdf_pages(pdf_file, output_path, page_data, report_name_template):
    """
    Extract pages from a PDF file based on start and end page numbers.
    
    Args:
        pdf_file (str): Path to the input PDF file
        output_path (str): Directory to save extracted PDFs
        page_data (DataFrame): DataFrame with start, end pages and other metadata
        report_name_template (str): Template for naming output files, e.g., "OncoKids_{year}_{specimen}.pdf"
    """
    with open(pdf_file, "rb") as infile:
        reader = PdfReader(infile)
        
        # Iterate through each row in the DataFrame
        for index, row in page_data.iterrows():
            writer = PdfWriter()
            
            # Extract pages between 'start_page' and 'end_page'
            for page_num in range(row['start_page_number'] - 1, row['end_page_number']):
                writer.add_page(reader.pages[page_num])
            
            # Construct the output filename with the specified template
            specimen = row["Specimen"]
            year = row.get("year", "")  # Get year if available, otherwise empty string
            output_filename = report_name_template.format(year=year, specimen=specimen)
            
            # Save the PDF
            with open(output_filename, "wb") as outfile:
                writer.write(outfile)