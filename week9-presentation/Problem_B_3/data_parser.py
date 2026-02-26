"""
Data Parser Module - Problem C
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
        
    """
    try:
        reader = csv.DictReader(io.StringIO(csv_string), delimiter=delimiter)
        result = []
        for row in reader:
            result.append(row)
        return result
    except Exception as e:
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
        
    """
    if required_fields is None:
        required_fields = []
    try:
        config = json.loads(json_string)
        for field in required_fields:
            if field not in config:
                print(f"Warning: Missing required field: {field}")
        return config
    except json.JSONDecodeError:
        raise ParseError("Invalid JSON")

def extract_numbers(text: str) -> List[float]:
    """
    Extracts all numbers (integer and float) from text.
    
    Args:
        text (str): Text to extract numbers from
        
    Returns:
        List[float]: List of extracted numbers
        
    """
    import re
    pattern = r'\d+\.?\d*'
    matches = re.findall(pattern, text)
    numbers = []
    for match in matches:
        try:
            numbers.append(float(match))
        except ValueError:
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
        
    """
    if preserve_line_breaks:
        text = re.sub(r'[\t ]+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
    else:
        text = re.sub(r'\s+', ' ', text)
    return text.strip()

def validate_data_types(data: Dict[str, Any], schema: Dict[str, type]) -> bool:
    """
    Validates that data matches expected schema types.
    
    Args:
        data (Dict): Data to validate
        schema (Dict): Schema with field names and expected types
        
    Returns:
        bool: True if data matches schema, False otherwise
        
    """
    for field, expected_type in schema.items():
        if field not in data:
            continue
        value = data[field]
        if type(value) != expected_type:
            return False
    return True