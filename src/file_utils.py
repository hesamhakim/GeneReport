"""
Utilities for file operations, including finding files with specified patterns.
"""

import os
import glob

def get_matching_files(directory, pattern):
    """
    Get all files in directory matching the given pattern.
    
    Args:
        directory (str): Directory to search
        pattern (str): File pattern to match (e.g., "*.pdf")
    
    Returns:
        list: List of file paths matching the pattern
    """
    return glob.glob(os.path.join(directory, pattern))

def ensure_directory_exists(directory):
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory (str): Directory path
    """
    os.makedirs(directory, exist_ok=True)