"""Utility functions for Apple Pass generation"""

from datetime import datetime


def rgb_color(r: int, g: int, b: int) -> str:
    """Helper to create RGB color string
    
    Creates an RGB color string in the format "rgb(r, g, b)" for use in
    Apple Wallet passes. All color values must be integers between 0 and 255.
    
    Args:
        r (int): Red value (0-255)
        g (int): Green value (0-255)
        b (int): Blue value (0-255)
    
    Returns:
        str: RGB color string in format "rgb(r, g, b)"
    
    Raises:
        ValueError: If any RGB value is not an integer or not in range 0-255
    
    Example:
        >>> rgb_color(255, 110, 0)
        'rgb(255, 110, 0)'
        >>> rgb_color(0, 0, 0)  # Black
        'rgb(0, 0, 0)'
        >>> rgb_color(255, 255, 255)  # White
        'rgb(255, 255, 255)'
    """
    # Validate that all values are integers
    if not all(isinstance(val, int) for val in [r, g, b]):
        raise ValueError("RGB values must be integers")
    
    # Validate range
    if not all(0 <= val <= 255 for val in [r, g, b]):
        raise ValueError("RGB values must be between 0 and 255")
    
    return f"rgb({r}, {g}, {b})"


def hex_to_rgb(hex_color: str) -> str:
    """Convert hex color to RGB format
    
    Converts a hexadecimal color code to an RGB color string suitable for
    Apple Wallet passes. Supports both 3-digit (#RGB) and 6-digit (#RRGGBB)
    hex formats, with or without the "#" prefix.
    
    Args:
        hex_color (str): Hex color (e.g., "#FF6E00", "FF6E00", "#F60", "F60")
    
    Returns:
        str: RGB color string in format "rgb(r, g, b)"
    
    Raises:
        ValueError: If hex color format is invalid
    
    Example:
        >>> hex_to_rgb("#FF6E00")
        'rgb(255, 110, 0)'
        >>> hex_to_rgb("FF6E00")
        'rgb(255, 110, 0)'
        >>> hex_to_rgb("#F60")  # 3-digit format
        'rgb(255, 102, 0)'
        >>> hex_to_rgb("F60")
        'rgb(255, 102, 0)'
    """
    if not isinstance(hex_color, str):
        raise ValueError("Hex color must be a string")
    
    # Remove leading '#' if present
    hex_color = hex_color.lstrip('#')
    
    # Validate hex color length
    if len(hex_color) not in (3, 6):
        raise ValueError("Hex color must be 3 or 6 characters (excluding '#')")
    
    # Validate hex characters
    try:
        int(hex_color, 16)
    except ValueError:
        raise ValueError(f"Invalid hex color: '{hex_color}' contains non-hex characters")
    
    # Expand 3-digit hex to 6-digit
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    # Convert to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    return rgb_color(r, g, b)


def format_iso8601(dt: datetime, timezone_offset: str = "+00:00") -> str:
    """Format datetime to ISO 8601 string for passes
    
    Formats a Python datetime object to an ISO 8601 formatted string with
    timezone offset, as required by Apple Wallet passes. The format is:
    YYYY-MM-DDTHH:MM:SS[timezone_offset]
    
    Args:
        dt (datetime): Python datetime object to format
        timezone_offset (str): Timezone offset in format "+HH:MM" or "-HH:MM"
                              (default: "+00:00" for UTC)
    
    Returns:
        str: ISO 8601 formatted string with timezone
    
    Raises:
        ValueError: If dt is not a datetime object or timezone_offset is invalid
    
    Example:
        >>> from datetime import datetime
        >>> format_iso8601(datetime(2026, 3, 15, 19, 0, 0), "-08:00")
        '2026-03-15T19:00:00-08:00'
        >>> format_iso8601(datetime(2026, 12, 31, 23, 59, 59), "+00:00")
        '2026-12-31T23:59:59+00:00'
        >>> format_iso8601(datetime(2026, 6, 1, 12, 30, 0), "+05:30")
        '2026-06-01T12:30:00+05:30'
    """
    if not isinstance(dt, datetime):
        raise ValueError("dt must be a datetime object")
    
    if not isinstance(timezone_offset, str):
        raise ValueError("timezone_offset must be a string")
    
    # Validate timezone offset format
    if not _is_valid_timezone_offset(timezone_offset):
        raise ValueError(
            "timezone_offset must be in format '+HH:MM' or '-HH:MM' "
            f"(e.g., '+00:00', '-08:00'), got: '{timezone_offset}'"
        )
    
    # Format datetime to ISO 8601
    base = dt.strftime("%Y-%m-%dT%H:%M:%S")
    return f"{base}{timezone_offset}"


def _is_valid_timezone_offset(offset: str) -> bool:
    """Validate timezone offset format
    
    Args:
        offset (str): Timezone offset string to validate
    
    Returns:
        bool: True if valid format, False otherwise
    """
    if len(offset) != 6:
        return False
    
    if offset[0] not in ('+', '-'):
        return False
    
    if offset[3] != ':':
        return False
    
    try:
        hours = int(offset[1:3])
        minutes = int(offset[4:6])
        
        # Validate hours (0-14) and minutes (0-59)
        # Note: UTC+14 is the maximum timezone offset (Kiribati)
        if not (0 <= hours <= 14):
            return False
        if not (0 <= minutes <= 59):
            return False
        
        # For UTC+14, minutes must be 0
        if hours == 14 and minutes != 0:
            return False
        
        return True
    except ValueError:
        return False
