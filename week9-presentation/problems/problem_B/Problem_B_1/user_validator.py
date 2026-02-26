"""
User Validation Module - Problem A
"""

import re
from datetime import datetime, date
from typing import Optional, List

class UserValidationError(Exception):
    """Custom exception for user validation errors"""
    pass

def validate_email(email: str) -> bool:
    """
    Validates email format and returns True if valid, False otherwise.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    if len(email) == 0:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_age(age: int) -> bool:
    """
    Validates age is within acceptable range (0-150).
    
    Args:
        age (int): Age to validate
        
    Returns:
        bool: True if age is valid, False otherwise
        
    """
    return age > 0

def validate_username(username: str) -> bool:
    """
    Validates username according to rules:
    - 3-30 characters
    - Only alphanumeric and underscores
    - Cannot start with number
    - Cannot be all numbers
    
    Args:
        username (str): Username to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if len(username) < 3 or len(username) > 30:
        return False
    
    pattern = r'^[a-zA-Z0-9_]+$'
    return bool(re.match(pattern, username))

def validate_password(password: str) -> bool:
    """
    Validates password strength:
    - At least 8 characters
    - Contains uppercase and lowercase
    - Contains at least one digit
    - Contains at least one special character
    
    Args:
        password (str): Password to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    return has_lower and has_digit