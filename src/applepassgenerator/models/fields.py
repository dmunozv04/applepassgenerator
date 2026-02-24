"""
Field classes for Apple Wallet Pass information display.

This module contains field classes used to define the information displayed
on passes, including:
- Field: Base field class for all pass information
- DateField: For displaying dates and times
- NumberField: For displaying formatted numbers
- CurrencyField: For displaying currency amounts

All field classes support iOS 6.0+ features with progressive enhancement
for newer iOS versions (iOS 7.0+, iOS 10.0+, iOS 12.0+).
"""

from typing import Any, Dict, List, Optional

from .constants import Alignment, DateStyle, NumberStyle


class Field:
    """Base field class for pass information display.
    
    Fields are the building blocks of pass content, appearing in various
    sections (header, primary, secondary, auxiliary, back). Each field
    displays a key-value pair with optional label and formatting.
    
    iOS Version Support:
        - iOS 6.0+: Basic fields with key, value, label, changeMessage, textAlignment
        - iOS 7.0+: attributedValue for HTML-formatted text
        - iOS 10.0+: dataDetectorTypes for auto-detecting phone numbers, links, etc.
        - iOS 12.0+: semantics for semantic tags (event info, transit details, etc.)
    
    Attributes:
        key (str): Required. Unique identifier for the field within the pass.
        value: Required. The field's value (string, number, or date).
        label (str): Optional. Label text displayed above the value.
        changeMessage (str): Optional. Format string for update alert text.
            Use %@ as placeholder for the field's new value.
        textAlignment (str): Optional. Text alignment (use Alignment constants).
            Default is PKTextAlignmentLeft.
        attributedValue (str): Optional. iOS 7.0+. HTML-formatted value with
            markup for bold, italic, etc. Overrides the value attribute.
        dataDetectorTypes (List[str]): Optional. iOS 10.0+. List of data detector
            types for automatic link detection (phone numbers, addresses, etc.).
            Use DataDetectorType constants.
        semantics (object): Optional. iOS 12.0+. SemanticTags object for
            structured semantic information. Set to None initially; will be
            added when semantic tags module is implemented.
    
    Example:
        >>> field = Field(
        ...     key="boardingTime",
        ...     value="3:45 PM",
        ...     label="Boarding Time",
        ...     changeMessage="Boarding time changed to %@"
        ... )
        >>> field.textAlignment = Alignment.CENTER
        >>> field.dataDetectorTypes = [DataDetectorType.CALENDAR_EVENT]
    """
    
    def __init__(
        self,
        key: str,
        value: Any,
        label: str = "",
    ) -> None:
        """Initialize a field with key, value, and optional label.
        
        Args:
            key: Unique identifier for the field. Required.
            value: The field's value. Can be string, number, or ISO 8601 date. Required.
            label: Label text for the field. Optional, defaults to empty string.
        """
        # Required attributes (iOS 6.0+)
        self.key = key
        self.value = value
        self.label = label
        
        # Optional attributes
        self.changeMessage = None
        self.textAlignment = None
        
        # iOS 7.0+ attributes
        self.attributedValue: Optional[str] = None
        
        # iOS 10.0+ attributes
        self.dataDetectorTypes: Optional[List[str]] = None
        
        # iOS 12.0+ attributes
        # Note: semantics will reference SemanticTags class when implemented
        self.semantics: Optional[Any] = None
    
    def json_dict(self) -> Dict[str, Any]:
        """Generate JSON dictionary representation for pass.json.
        
        Converts the field to a dictionary suitable for JSON serialization,
        excluding None values and empty strings to minimize pass size.
        Special handling for:
        - semantics: Calls json_dict() if object has the method
        - dataDetectorTypes: Included only if non-empty list
        - All other attributes: Included if not None and not empty string
        
        Returns:
            Dictionary with non-None, non-empty field attributes.
        """
        d = {}
        for attr_key, attr_value in self.__dict__.items():
            # Skip None values and empty strings
            if attr_value is None or attr_value == "":
                continue
            
            # Handle semantic tags specially (convert to JSON)
            if attr_key == 'semantics' and hasattr(attr_value, 'json_dict'):
                d[attr_key] = attr_value.json_dict()
            # Handle list of data detector types (only if non-empty)
            elif attr_key == 'dataDetectorTypes' and isinstance(attr_value, list):
                if attr_value:  # Only add if list is not empty
                    d[attr_key] = attr_value
            else:
                d[attr_key] = attr_value
        return d


class DateField(Field):
    """Field for displaying dates and times with localized formatting.
    
    DateField extends Field to provide specialized date and time display
    options. Supports various display styles (short, medium, long, full)
    for both date and time components, relative date display, and timezone
    handling.
    
    iOS Version Support:
        - iOS 6.0+: Basic date/time display with dateStyle and timeStyle
        - iOS 6.0+: isRelative for relative date display ("2 hours ago")
        - iOS 7.0+: ignoresTimeZone to display date in pass's timezone
    
    Attributes:
        dateStyle (str): Style for date display. Use DateStyle constants
            (NONE, SHORT, MEDIUM, LONG, FULL). Default is SHORT.
        timeStyle (str): Style for time display. Use DateStyle constants.
            Default is SHORT.
        isRelative (bool): If True, display as relative date ("in 2 hours").
            Default is False.
        ignoresTimeZone (bool): iOS 7.0+. If True, display date in pass's
            timezone instead of user's current timezone. Only set if True.
    
    Value Format:
        The value should be an ISO 8601 date string (e.g., "2026-02-12T15:30:00Z")
        or a datetime object that will be serialized to ISO 8601 format.
    
    Example:
        >>> date_field = DateField(
        ...     key="departureTime",
        ...     value="2026-02-12T15:30:00-08:00",
        ...     label="Departure",
        ...     date_style=DateStyle.MEDIUM,
        ...     time_style=DateStyle.SHORT,
        ...     ignores_time_zone=True
        ... )
    """
    
    def __init__(
        self,
        key: str,
        value: Any,
        label: str = "",
        date_style: str = DateStyle.SHORT,
        time_style: str = DateStyle.SHORT,
        ignores_time_zone: bool = False,
        is_relative: bool = False,
    ) -> None:
        """Initialize a date field with date/time formatting options.
        
        Args:
            key: Unique identifier for the field. Required.
            value: ISO 8601 date string or datetime object. Required.
            label: Label text for the field. Optional.
            date_style: Date display style (use DateStyle constants). Default is SHORT.
            time_style: Time display style (use DateStyle constants). Default is SHORT.
            ignores_time_zone: If True, display in pass timezone (iOS 7.0+). Default is False.
            is_relative: If True, display as relative date. Default is False.
        """
        super(DateField, self).__init__(key, value, label)
        
        # Date/time formatting (iOS 6.0+)
        self.dateStyle = date_style
        self.timeStyle = time_style
        self.isRelative = is_relative
        
        # iOS 7.0+: Only set ignoresTimeZone if True (to minimize pass size)
        if ignores_time_zone:
            self.ignoresTimeZone = ignores_time_zone


class NumberField(Field):
    """Field for displaying formatted numbers.
    
    NumberField extends Field to provide number-specific formatting options
    such as decimal, percentage, scientific notation, or spelled-out numbers.
    
    iOS Version Support:
        - iOS 6.0+: Number formatting with numberStyle
    
    Attributes:
        numberStyle (str): Number display style. Use NumberStyle constants:
            - DECIMAL: Standard decimal notation (default)
            - PERCENT: Percentage (multiply by 100, add % symbol)
            - SCIENTIFIC: Scientific notation
            - SPELLOUT: Spelled out ("forty-two")
    
    Value Format:
        The value should be a number (int or float). For percentage display,
        use the decimal value (e.g., 0.42 for 42%).
    
    Example:
        >>> number_field = NumberField(
        ...     key="score",
        ...     value=95.5,
        ...     label="Score",
        ...     number_style=NumberStyle.DECIMAL
        ... )
        >>> 
        >>> percent_field = NumberField(
        ...     key="discount",
        ...     value=0.15,
        ...     label="Discount",
        ...     number_style=NumberStyle.PERCENT
        ... )
    """
    
    def __init__(
        self,
        key: str,
        value: Any,
        label: str = "",
        number_style: str = NumberStyle.DECIMAL,
    ) -> None:
        """Initialize a number field with formatting options.
        
        Args:
            key: Unique identifier for the field. Required.
            value: Numeric value (int or float). Required.
            label: Label text for the field. Optional.
            number_style: Number display style (use NumberStyle constants).
                Default is DECIMAL.
        """
        super(NumberField, self).__init__(key, value, label)
        self.numberStyle = number_style


class CurrencyField(NumberField):
    """Field for displaying currency amounts with proper formatting.
    
    CurrencyField extends NumberField to provide automatic currency formatting
    based on ISO 4217 currency codes. The amount is displayed with appropriate
    currency symbol and decimal precision.
    
    iOS Version Support:
        - iOS 6.0+: Currency display with currencyCode
    
    Attributes:
        currencyCode (str): ISO 4217 currency code (e.g., "USD", "EUR", "GBP").
            Determines the currency symbol and formatting rules.
    
    Value Format:
        The value should be a numeric amount in the specified currency.
        Do not include currency symbols in the value itself.
    
    Example:
        >>> currency_field = CurrencyField(
        ...     key="balance",
        ...     value=1234.56,
        ...     label="Account Balance",
        ...     currency_code="USD"
        ... )
        >>> # Will display as: $1,234.56
        >>>
        >>> euro_field = CurrencyField(
        ...     key="price",
        ...     value=42.99,
        ...     label="Price",
        ...     currency_code="EUR"
        ... )
        >>> # Will display as: €42.99
    """
    
    def __init__(
        self,
        key: str,
        value: Any,
        label: str = "",
        currency_code: str = "",
    ) -> None:
        """Initialize a currency field with currency code.
        
        Args:
            key: Unique identifier for the field. Required.
            value: Numeric currency amount. Required.
            label: Label text for the field. Optional.
            currency_code: ISO 4217 currency code (e.g., "USD"). Optional but
                recommended for proper currency display.
        """
        super(CurrencyField, self).__init__(key, value, label)
        self.currencyCode = currency_code
