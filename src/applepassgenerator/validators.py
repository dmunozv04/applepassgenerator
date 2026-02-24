"""Input validation for Apple Pass fields"""

import re


def validate_iso8601_date(date_string):
    """Validate ISO 8601 date format
    
    Args:
        date_string (str): Date string to validate
    
    Returns:
        bool: True if valid
    
    Raises:
        ValueError: If invalid format
    
    Example:
        >>> validate_iso8601_date("2026-03-15T19:00:00-08:00")
        True
    """
    if not isinstance(date_string, str):
        raise ValueError(f"Date must be a string, got {type(date_string).__name__}")
    
    # Basic ISO 8601 regex
    pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$'
    if not re.match(pattern, date_string):
        raise ValueError(f"Invalid ISO 8601 date format: {date_string}")
    return True


def validate_rgb_color(color_string):
    """Validate RGB color format: rgb(r, g, b)
    
    Args:
        color_string (str): Color string to validate
    
    Returns:
        bool: True if valid
    
    Raises:
        ValueError: If invalid format
    
    Example:
        >>> validate_rgb_color("rgb(255, 110, 0)")
        True
    """
    if not isinstance(color_string, str):
        raise ValueError(f"Color must be a string, got {type(color_string).__name__}")
    
    pattern = r'^rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)$'
    if not re.match(pattern, color_string):
        raise ValueError(f"Invalid RGB format: {color_string}. Expected: rgb(r, g, b)")
    
    # Extract values and validate range (0-255)
    values = re.findall(r'\d+', color_string)
    for val in values:
        if int(val) > 255:
            raise ValueError(f"RGB values must be 0-255: {color_string}")
    return True


def validate_currency_code(code):
    """Validate ISO 4217 currency code
    
    Args:
        code (str): Currency code (e.g., "USD")
    
    Returns:
        bool: True if valid format (3 uppercase letters)
    
    Raises:
        ValueError: If invalid format
    
    Example:
        >>> validate_currency_code("USD")
        True
    """
    if not isinstance(code, str):
        raise ValueError(f"Currency code must be a string, got {type(code).__name__}")
    
    if not re.match(r'^[A-Z]{3}$', code):
        raise ValueError(f"Invalid ISO 4217 currency code: {code}")
    return True


def validate_location_limits(locations_list):
    """Ensure locations list doesn't exceed Apple's limit
    
    Args:
        locations_list (list): List of Location objects
    
    Returns:
        bool: True if valid
    
    Raises:
        ValueError: If more than 10 locations
    
    Example:
        >>> validate_location_limits([1, 2, 3])
        True
    """
    if not isinstance(locations_list, list):
        raise ValueError(f"Locations must be a list, got {type(locations_list).__name__}")
    
    if len(locations_list) > 10:
        raise ValueError("Apple Wallet passes support maximum 10 locations")
    return True


def validate_beacon_limits(beacons_list):
    """Ensure beacons list doesn't exceed Apple's limit
    
    Args:
        beacons_list (list): List of IBeacon objects
    
    Returns:
        bool: True if valid
    
    Raises:
        ValueError: If more than 10 beacons
    
    Example:
        >>> validate_beacon_limits([1, 2, 3])
        True
    """
    if not isinstance(beacons_list, list):
        raise ValueError(f"Beacons must be a list, got {type(beacons_list).__name__}")
    
    if len(beacons_list) > 10:
        raise ValueError("Apple Wallet passes support maximum 10 beacons")
    return True


def validate_serial_number(serial_number):
    """Validate serial number
    
    Args:
        serial_number (str): Serial number
    
    Returns:
        bool: True if valid
    
    Raises:
        ValueError: If empty or invalid
    
    Example:
        >>> validate_serial_number("ABC123456")
        True
    """
    if not serial_number or not isinstance(serial_number, str):
        raise ValueError("serial_number is required and must be a non-empty string")
    return True


def validate_authentication_token(token):
    """Validate web service authentication token
    
    Args:
        token (str): Authentication token
    
    Returns:
        bool: True if valid
    
    Raises:
        ValueError: If less than 16 characters
    
    Example:
        >>> validate_authentication_token("my_secure_token_12345")
        True
    """
    if not isinstance(token, str):
        raise ValueError(f"Authentication token must be a string, got {type(token).__name__}")
    
    if len(token) < 16:
        raise ValueError("authenticationToken must be at least 16 characters")
    return True
