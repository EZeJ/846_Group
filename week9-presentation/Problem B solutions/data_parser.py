"""
Data Parser Module - Problem C
Functions with various edge cases perfect for boundary testing
Contains intentional bugs in edge case handling
"""

import json
import csv
from typing import List, Dict, Any, Optional
from datetime import datetime
import io

class ParseError(Exception):
    """Custom exception for parsing errors"""
    pass

def parse_csv_data(csv_string: str, delimiter: str = ",") -> List[Dict[str, str]]:
    """
    Parses CSV data and returns list of dictionaries.
    
    Args:
        csv_string (str): CSV data as string
        delimiter (str): Field delimiter (default: comma)
        
    Returns:
        List[Dict[str, str]]: Parsed data as list of dictionaries
        
    Raises:
        ParseError: When CSV parsing fails
        
    Intentional Bugs: Edge cases not handled properly
    """
    # Bug 24: No null check for csv_string
    # Bug 25: No empty string check
    
    try:
        # Bug 26: Doesn't handle empty files or files with only headers
        reader = csv.DictReader(io.StringIO(csv_string), delimiter=delimiter)
        result = []
        
        for row in reader:
            # Bug 27: Doesn't handle rows with missing fields
            result.append(row)
            
        return result
    except Exception as e:
        # Bug 28: Generic exception handling
        raise ParseError("CSV parsing failed")

def parse_json_config(json_string: str, required_fields: List[str] = None) -> Dict[str, Any]:
    """
    Parses JSON configuration and validates required fields.
    
    Args:
        json_string (str): JSON data as string
        required_fields (List[str], optional): List of required field names
        
    Returns:
        Dict[str, Any]: Parsed configuration
        
    Raises:
        ParseError: When JSON is invalid or required fields missing
        
    Intentional Bugs: Validation logic has flaws
    """
    # Bug 29: No null check for json_string
    if required_fields is None:
        required_fields = []
    
    try:
        config = json.loads(json_string)
        
        # Bug 30: Doesn't check if config is a dict (could be list, string, etc.)
        
        # Bug 31: Required field validation has logic error
        for field in required_fields:
            if field not in config:
                # Bug 32: Should raise exception but continues
                print(f"Warning: Missing required field: {field}")
        
        return config
        
    except json.JSONDecodeError:
        # Bug 33: Doesn't provide helpful error message
        raise ParseError("Invalid JSON")

def extract_numbers(text: str) -> List[float]:
    """
    Extracts all numbers (integer and float) from text.
    
    Args:
        text (str): Text to extract numbers from
        
    Returns:
        List[float]: List of extracted numbers
        
    Intentional Bugs: Number extraction logic has issues
    """
    # Bug 34: No null check
    # Bug 35: Doesn't handle empty string
    
    import re
    
    # Bug 36: Regex pattern doesn't handle negative numbers
    # Bug 37: Doesn't handle scientific notation (e.g., 1.5e10)
    pattern = r'\d+\.?\d*'
    
    matches = re.findall(pattern, text)
    numbers = []
    
    for match in matches:
        try:
            # Bug 38: Doesn't handle edge case where match is just a dot "."
            numbers.append(float(match))
        except ValueError:
            # Bug 39: Silently ignores conversion errors
            pass
    
    return numbers

def normalize_whitespace(text: str, preserve_line_breaks: bool = False) -> str:
    """
    Normalizes whitespace in text - removes extra spaces and tabs.
    
    Args:
        text (str): Text to normalize
        preserve_line_breaks (bool): Whether to preserve line breaks
        
    Returns:
        str: Text with normalized whitespace
        
    Intentional Bugs: Whitespace handling edge cases
    """
    # Bug 40: No null check
    # Bug 41: Doesn't handle empty string properly
    
    if preserve_line_breaks:
        # Bug 42: Logic error - replaces line breaks when it should preserve them
        text = re.sub(r'[\t ]+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
    else:
        # Bug 43: Doesn't handle all types of whitespace (e.g., \r, \f, \v)
        text = re.sub(r'\s+', ' ', text)
    
    # Bug 44: strip() may remove important leading/trailing spaces in some contexts
    return text.strip()

def validate_data_types(data: Dict[str, Any], schema: Dict[str, type]) -> bool:
    """
    Validates that data matches expected schema types.
    
    Args:
        data (Dict): Data to validate
        schema (Dict): Schema with field names and expected types
        
    Returns:
        bool: True if data matches schema, False otherwise
        
    Intentional Bugs: Type validation logic issues
    """
    # Bug 45: No null checks
    # Bug 46: Doesn't check if data is actually a dict
    
    for field, expected_type in schema.items():
        if field not in data:
            # Bug 47: Missing fields should probably fail validation
            continue
            
        value = data[field]
        
        # Bug 48: Type checking logic is flawed
        if type(value) != expected_type:
            # Bug 49: Doesn't handle None values appropriately
            # Bug 50: Doesn't handle inheritance (e.g., bool is instance of int in Python)
            return False
    
    return True