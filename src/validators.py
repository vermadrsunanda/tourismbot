"""
Input validation and sanitization utilities.
"""
import re
from typing import Any, Optional


def validate_and_sanitize_input(user_input: Any, max_length: int = 1000) -> Optional[str]:
    """
    Validate and sanitize user input.
    
    Args:
        user_input: Input to validate
        max_length: Maximum allowed input length
    
    Returns:
        Sanitized input or None if invalid
    """
    # Type checking
    if not isinstance(user_input, str):
        return None
    
    # Strip whitespace
    sanitized = user_input.strip()
    
    # Check length
    if len(sanitized) == 0 or len(sanitized) > max_length:
        return None
    
    # Remove potentially harmful characters but allow normal text
    # Allow letters, numbers, spaces, and common punctuation
    sanitized = re.sub(r'[^\w\s\-.,!?\'"]', '', sanitized)
    
    return sanitized


def validate_destination_name(destination: str) -> bool:
    """
    Validate destination name format.
    
    Args:
        destination: Destination name to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(destination, str):
        return False
    
    destination = destination.strip()
    
    # Allow letters, spaces, hyphens, and apostrophes
    pattern = r'^[a-zA-Z\s\-\']+$'
    return bool(re.match(pattern, destination)) and len(destination) > 0


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(email, str):
        return False
    
    # Simple email validation pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))
