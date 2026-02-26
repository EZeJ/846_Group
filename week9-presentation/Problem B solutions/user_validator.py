"""
User Validation Module - Problem A
Contains intentional bugs that will be caught by proper boundary and negative testing
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
        
    Intentional Bug: Does not handle None/empty inputs properly
    """
    # Bug 1: No null/empty check - will crash on None
    if len(email) == 0:
        return False
        
    # Bug 2: Regex doesn't handle edge cases like consecutive dots
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_age(age: int) -> bool:
    """
    Validates age is within acceptable range (0-150).
    
    Args:
        age (int): Age to validate
        
    Returns:
        bool: True if age is valid, False otherwise
        
    Intentional Bugs: Boundary conditions not handled properly
    """
    # Bug 3: Should be >= 0, but uses > 0 (excludes newborns) and should be <= 150
    # Bug 4: Email validation allows to start from special character
    # Bug 5: No upper bound check (should be <= 150)
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
        
    Intentional Bugs: Multiple edge cases not handled
    """
    # Bug 6: No null check
    # Bug 7: Length check uses < 3 instead of <= 2
    if len(username) < 3 or len(username) > 30:
        return False
    
    # Bug 8: Doesn't check if starts with number
    # Bug 9: Doesn't check if all numbers
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
        
    Intentional Bugs: Missing checks and edge cases
    """
    # Bug 10: No null check
    # Bug 11: Length check incorrect (< 8 instead of <= 7)
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    # Bug 12: Special character check missing
    # Bug 13: Returns True even if missing uppercase
    return has_lower and has_digit