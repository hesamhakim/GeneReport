"""
Utilities for integrating DNA, RNA, and CMA data from multiple CSV files.
"""

import pandas as pd
import os
import re
from IPython.display import display
from datetime import datetime

def standardize_and_merge_dna_data(input_directory, output_directory, output_filename, table_type):
    """
    Standardizes and merges CSV files containing DNA variant data.
    
    Parameters:
    input_directory (str): Full path to input directory containing CSV files
    output_directory (str): Full path to output directory for saving results
    output_filename (str): Name of the output file (should end with .csv)
    table_type (str): Type of analysis for metadata
    
    Returns:
    pandas.DataFrame: Combined and standardized data
    """
    # Validate input and output directories
    if not os.path.exists(input_directory):
        raise ValueError(f"Input directory does not exist: {input_directory}")
    
    # Validate output filename
    if not output_filename.endswith('.csv'):
        output_filename += '.csv'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Display directory information
    display("#### Directory Information")
    dir_info = pd.DataFrame({
        'Parameter': ['Input Directory', 'Output Directory', 'Output Filename'],
        'Path': [input_directory, output_directory, output_filename]
    })
    display(dir_info)
    
    dfs_to_concatenate = []
    
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_directory, filename)
            try:
                # Detect if file has headers
                with open(file_path, 'r') as f:
                    first_line = f.readline().strip()
                    has_headers = not any(pattern in first_line.lower() 
                                        for pattern in ['signif', 'p.', 'c.', 'nm_', '%', 'chr'])
                
                # Read file accordingly
                if has_headers:
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_csv(file_path, header=None)
                
                # Clean line breaks in all columns
                for column in df.columns:
                    df[column] = df[column].astype(str).apply(
                        lambda x: ' '.join(x.split()))
                
                # Check column count
                if not (6 < len(df.columns) < 9):
                    display(f"⚠️ Skipping {filename}: Column count not between 6 and 9")
                    continue
                
                # Create a mapping of column positions/names to standard names
                column_mapping = {}
                
                # Find columns based on content patterns
                for col in df.columns:
                    col_values = df[col].astype(str)
                    
                    if col_values.str.contains('signif', case=False).any():
                        column_mapping[col] = "Classification"
                    elif col_values.str.contains('^p\.', regex=True).any():
                        column_mapping[col] = "Protein Change"
                    elif col_values.str.contains(r'\d+%', regex=True).any():
                        column_mapping[col] = "Variant Allele Frequency"
                    elif col_values.str.contains('^c\.', regex=True).any():
                        column_mapping[col] = "DNA Change"
                    elif col_values.str.contains('^NM_', regex=True).any():
                        column_mapping[col] = "DNA Change NM"
                    elif col_values.str.match(r'^[A-Z][A-Z0-9-]{0,5}$').any():
                        column_mapping[col] = "Gene Name"
                    elif col_values.str.contains(r'chr|^\d{1,3}(?:,\d{3})+$', regex=True).any():
                        column_mapping[col] = "Genomic Position (hg19)"
                    elif col_values.str.match(r'^(\d{1,3}|intron.*)$', case=False).any():
                        column_mapping[col] = "Exon"
                
                # Check if required columns were found
                if "Classification" not in column_mapping.values():
                    display(f"⚠️ Skipping {filename}: No 'signif' column found")
                    continue
                
                # Rename the identified columns and drop duplicates if any
                df = df.rename(columns=column_mapping)
                df = df.loc[:, ~df.columns.duplicated()]
                
                # Add metadata columns
                df["table_type"] = table_type
                df["report_name"] = filename
                
                dfs_to_concatenate.append(df)
                display(f"✓ Successfully processed {filename}")
                display(f"Mapped columns: {column_mapping}")
                
            except Exception as e:
                display(f"⚠️ Error processing {filename}: {str(e)}")
    
    if dfs_to_concatenate:
        try:
            # Concatenate all dataframes
            result_df = pd.concat(dfs_to_concatenate, ignore_index=True)
            
            # Create full output path
            output_path = os.path.join(os.path.abspath(output_directory), output_filename)
            
            # Save the results with explicit encoding
            result_df.to_csv(output_path, index=False, encoding='utf-8')
            display(f"🔄 Results successfully saved to: {output_path}")
            
            # Display output file information
            display("#### Output File Information")
            output_info = pd.DataFrame({
                'Information': ['Output Directory', 'File Name', 'Full Path'],
                'Value': [output_directory, output_filename, output_path]
            })
            display(output_info)
            
            return result_df
            
        except Exception as e:
            display(f"⚠️ Error saving results: {str(e)}")
            return pd.DataFrame()
    else:
        display("No matching files found")
        return pd.DataFrame()

def standardize_and_merge_rna_data(input_directory, output_directory, output_filename, table_type):
    """
    Standardizes and merges CSV files containing RNA fusion data with exactly two columns.
    
    Parameters:
    input_directory (str): Full path to input directory containing CSV files
    output_directory (str): Full path to output directory for saving results
    output_filename (str): Name of the output file (should end with .csv)
    table_type (str): Type of analysis for metadata
    
    Returns:
    pandas.DataFrame: Combined and standardized data
    """
    # Validate input and output directories
    if not os.path.exists(input_directory):
        raise ValueError(f"Input directory does not exist: {input_directory}")
    
    # Validate output filename
    if not output_filename.endswith('.csv'):
        output_filename += '.csv'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Display directory information
    display("#### Directory Information")
    dir_info = pd.DataFrame({
        'Parameter': ['Input Directory', 'Output Directory', 'Output Filename'],
        'Path': [input_directory, output_directory, output_filename]
    })
    display(dir_info)
    
    dfs_to_concatenate = []
    
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_directory, filename)
            try:
                # Detect if file has headers
                with open(file_path, 'r') as f:
                    first_line = f.readline().strip()
                    has_headers = not any(pattern in first_line.lower() 
                                        for pattern in ['signif', 'p.', 'c.', 'nm_', '%', 'chr'])
                
                # Read file accordingly
                if has_headers:
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_csv(file_path, header=None)
                
                # Clean line breaks in all columns
                for column in df.columns:
                    df[column] = df[column].astype(str).apply(
                        lambda x: ' '.join(x.split()))
                
                # Check column count
                if len(df.columns) != 2:
                    display(f"⚠️ Skipping {filename}: Column count is not 2")
                    continue
                
                # Initialize column mapping
                column_mapping = {}
                
                # Assuming the first column is 'Classification' and the second is 'Fusion'
                if has_headers:
                    original_columns = df.columns.tolist()
                    column_mapping[original_columns[0]] = "Classification"
                    column_mapping[original_columns[1]] = "Fusion"
                else:
                    # If no headers, assign default names
                    column_mapping[df.columns[0]] = "Classification"
                    column_mapping[df.columns[1]] = "Fusion"
                
                # Rename columns
                df = df.rename(columns=column_mapping)
                
                # Verify that the renamed columns match the required names
                if set(df.columns) != {"Classification", "Fusion"}:
                    display(f"⚠️ Skipping {filename}: Columns could not be mapped to 'Classification' and 'Fusion'")
                    continue
                
                # Add metadata columns
                df["table_type"] = table_type
                df["report_name"] = filename
                
                dfs_to_concatenate.append(df)
                display(f"✓ Successfully processed {filename}")
                display(f"Mapped columns: {column_mapping}")
                
            except Exception as e:
                display(f"⚠️ Error processing {filename}: {str(e)}")
    
    if dfs_to_concatenate:
        try:
            # Concatenate all dataframes
            result_df = pd.concat(dfs_to_concatenate, ignore_index=True)
            
            # Create full output path
            output_path = os.path.join(os.path.abspath(output_directory), output_filename)
            
            # Save the results with explicit encoding
            result_df.to_csv(output_path, index=False, encoding='utf-8')
            display(f"🔄 Results successfully saved to: {output_path}")
            
            # Display output file information
            display("#### Output File Information")
            output_info = pd.DataFrame({
                'Information': ['Output Directory', 'File Name', 'Full Path'],
                'Value': [output_directory, output_filename, output_path]
            })
            display(output_info)
            
            return result_df
            
        except Exception as e:
            display(f"⚠️ Error saving results: {str(e)}")
            return pd.DataFrame()
    else:
        display("No matching files found")
        return pd.DataFrame()

def standardize_and_merge_cma_data(input_directory, output_directory, output_filename, table_type):
    """
    Standardizes and merges CSV files containing CMA data.
    
    Parameters:
    input_directory (str): Full path to input directory containing CSV files
    output_directory (str): Full path to output directory for saving results
    output_filename (str): Name of the output file (should end with .csv)
    table_type (str): Type of analysis for metadata
    
    Returns:
    pandas.DataFrame: Combined and standardized data
    """
    # Validate input and output directories
    if not os.path.exists(input_directory):
        raise ValueError(f"Input directory does not exist: {input_directory}")
    
    # Validate output filename
    if not output_filename.endswith('.csv'):
        output_filename += '.csv'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Display directory information
    display("#### Directory Information")
    dir_info = pd.DataFrame({
        'Parameter': ['Input Directory', 'Output Directory', 'Output Filename'],
        'Path': [input_directory, output_directory, output_filename]
    })
    display(dir_info)
    
    dfs_to_concatenate = []
    
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_directory, filename)
            try:
                # Detect if file has headers
                with open(file_path, 'r') as f:
                    first_line = f.readline().strip()
                    has_headers = not any(pattern in first_line.lower() 
                                        for pattern in ['signif', 'p.', 'c.', 'nm_', '%', 'chr'])
                
                # Read file accordingly
                if has_headers:
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_csv(file_path, header=None)
                
                # Clean line breaks in all columns
                for column in df.columns:
                    df[column] = df[column].astype(str).apply(
                        lambda x: ' '.join(x.split()))
                
                # Check if this looks like a CMA table with 2-5 columns
                if not (2 <= len(df.columns) <= 5):
                    display(f"⚠️ Skipping {filename}: Column count not between 2 and 5")
                    continue
                
                # Check if any columns contain "array" or "cma" keywords to ensure it's a CMA table
                contains_cma_keywords = False
                for col in df.columns:
                    col_values = df[col].astype(str).str.lower()
                    if col_values.str.contains('array|cma|chromosome|gain|loss|copy|genomic').any():
                        contains_cma_keywords = True
                        break
                
                if not contains_cma_keywords:
                    display(f"⚠️ Skipping {filename}: No CMA-related keywords found")
                    continue
                
                # Add metadata columns
                df["table_type"] = table_type
                df["report_name"] = filename
                
                dfs_to_concatenate.append(df)
                display(f"✓ Successfully processed {filename}")
                
            except Exception as e:
                display(f"⚠️ Error processing {filename}: {str(e)}")
    
    if dfs_to_concatenate:
        try:
            # Concatenate all dataframes
            result_df = pd.concat(dfs_to_concatenate, ignore_index=True)
            
            # Create full output path
            output_path = os.path.join(os.path.abspath(output_directory), output_filename)
            
            # Save the results with explicit encoding
            result_df.to_csv(output_path, index=False, encoding='utf-8')
            display(f"🔄 Results successfully saved to: {output_path}")
            
            # Display output file information
            display("#### Output File Information")
            output_info = pd.DataFrame({
                'Information': ['Output Directory', 'File Name', 'Full Path'],
                'Value': [output_directory, output_filename, output_path]
            })
            display(output_info)
            
            return result_df
            
        except Exception as e:
            display(f"⚠️ Error saving results: {str(e)}")
            return pd.DataFrame()
    else:
        display("No matching files found")
        return pd.DataFrame()


def integrate_cma_data(input_directory, output_directory, output_filename, table_type):
    """
    Integrates CSV files containing CMA (Chromosomal Microarray) data.
    
    Parameters:
    input_directory (str): Full path to input directory containing CSV files
    output_directory (str): Full path to output directory for saving results
    output_filename (str): Name of the output file (should end with .csv)
    table_type (str): Type of analysis for metadata
    
    Returns:
    pandas.DataFrame: Combined and standardized data
    """
    # Validate input and output directories
    if not os.path.exists(input_directory):
        raise ValueError(f"Input directory does not exist: {input_directory}")
    
    # Validate output filename
    if not output_filename.endswith('.csv'):
        output_filename += '.csv'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Display directory information
    display("#### Directory Information")
    dir_info = pd.DataFrame({
        'Parameter': ['Input Directory', 'Output Directory', 'Output Filename'],
        'Path': [input_directory, output_directory, output_filename]
    })
    display(dir_info)
    
    # Define the standard column names for CMA data
    standard_column_names = [
        "Copy State", "CNV Type", "Chromosome", "Start Band", "End Band",
        "Genomic position-Start", "Genomic position- End", "Size (kbp)",
        "Gene Count", "Relevant Cancer Genes/Comments"
    ]
    
    dfs_to_concatenate = []
    
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_directory, filename)
            try:
                # First try to read the file
                df = pd.read_csv(file_path)
                
                # Check if the file has enough columns to potentially be a CMA file
                if len(df.columns) < 5:  # CMA files typically have many columns
                    continue
                
                # Check if this is a CMA report by looking for key columns or patterns
                # This uses a positional check for the genomic position column which is often column 5 (index 5)
                col_num = 5  # The column to check (6th column, 0-indexed)
                regex_pattern = r"^\d+(,\d{3})*$"  # Pattern for formatted numbers
                
                # Check if column exists and then if it contains data matching our pattern
                if col_num < len(df.columns):
                    column_to_check = df.columns[col_num]
                    first_row = df.iloc[0] if not df.empty else None
                    
                    # Check if the column contains genomic position data
                    if first_row is not None and col_num < len(first_row):
                        if bool(re.search(regex_pattern, str(first_row.iloc[col_num]))):
                            # Determine if file has headers or not
                            if has_headers(df, col_num, regex_pattern):
                                # Has headers
                                if len(df.columns) == len(standard_column_names):
                                    df.columns = standard_column_names
                                else:
                                    display(f"⚠️ Skipping {filename}: Column count mismatch")
                                    continue
                            else:
                                # No headers, read the file again without headers
                                df = pd.read_csv(file_path, header=None)
                                if len(df.columns) == len(standard_column_names):
                                    df.columns = standard_column_names
                                else:
                                    display(f"⚠️ Skipping {filename}: Column count mismatch")
                                    continue
                            
                            # Check if the specified column contains any value matching the regex pattern
                            genome_pos_col = df.columns[col_num]
                            if df[genome_pos_col].astype(str).apply(lambda x: bool(re.search(regex_pattern, str(x)))).any():
                                # Add metadata columns
                                df["table_type"] = table_type
                                df["report_name"] = filename
                                
                                # Clean up any newline characters
                                df = df.replace('\n', ' ', regex=True)
                                
                                dfs_to_concatenate.append(df)
                                display(f"✓ Successfully processed {filename}")
                            else:
                                display(f"⚠️ Skipping {filename}: No matching pattern in specified column")
                    else:
                        # Skip this file - not a CMA report
                        continue
                        
            except Exception as e:
                display(f"⚠️ Error processing {filename}: {str(e)}")
    
    if dfs_to_concatenate:
        try:
            # Concatenate all dataframes
            result_df = pd.concat(dfs_to_concatenate, ignore_index=True)
            
            # Create full output path
            output_path = os.path.join(os.path.abspath(output_directory), output_filename)
            
            # Save the results with explicit encoding
            result_df.to_csv(output_path, index=False, encoding='utf-8')
            display(f"🔄 Results successfully saved to: {output_path}")
            
            # Display output file information
            display("#### Output File Information")
            output_info = pd.DataFrame({
                'Information': ['Output Directory', 'File Name', 'Full Path'],
                'Value': [output_directory, output_filename, output_path]
            })
            display(output_info)
            
            return result_df
            
        except Exception as e:
            display(f"⚠️ Error saving results: {str(e)}")
            return pd.DataFrame()
    else:
        display("No matching files found")
        return pd.DataFrame()

def has_headers(df, col_num, regex_pattern):
    """
    Determine if a DataFrame has headers by checking if the first row contains data.
    
    Parameters:
    df (pandas.DataFrame): DataFrame to check
    col_num (int): Column index to check for data pattern
    regex_pattern (str): Regular expression pattern that data should match
    
    Returns:
    bool: True if the DataFrame appears to have headers, False otherwise
    """
    if df.empty or col_num >= len(df.columns):
        return True  # Default to assuming headers if we can't check
    
    # Check the first row in the specified column
    first_row = df.iloc[0]
    if first_row.iloc[col_num] and bool(re.search(regex_pattern, str(first_row.iloc[col_num]))):
        return False  # No headers - first row contains data
    return True  # Has headers - first row doesn't match pattern