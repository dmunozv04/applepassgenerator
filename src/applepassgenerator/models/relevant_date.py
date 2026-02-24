"""
RelevantDate class for Apple Wallet Pass relevance.

This module provides the RelevantDate class for defining date-based relevance
for passes, allowing the system to display passes at appropriate times.
"""


class RelevantDate:
    """Date-based relevance for pass display.
    
    Represents a date interval that determines when a pass is relevant and should
    be displayed on the lock screen. You can either specify a single date (and
    Wallet auto-calculates an interval) or provide explicit start and end dates.
    
    iOS 18.0+ for relevantDates array
    iOS 6.0+ for singular relevantDate field (deprecated)
    
    Attributes:
        date (str): The date and time when the pass becomes relevant. 
            Wallet automatically calculates a relevancy interval from this date.
            Optional - use this OR startDate/endDate, not both.
        start_date (str): The date and time for the pass relevancy interval to begin.
            Optional - requires end_date when specified.
        end_date (str): The date and time for the pass relevancy interval to end.
            Optional - required when providing start_date.
    
    Examples:
        >>> # Simple date - Wallet auto-calculates interval
        >>> date = RelevantDate(date="2026-03-15T19:00:00-08:00")
        
        >>> # Explicit interval - doors open to show end
        >>> interval = RelevantDate(
        ...     start_date="2026-03-15T18:30:00-08:00",
        ...     end_date="2026-03-15T22:00:00-08:00"
        ... )
        
        >>> # Event with lead time
        >>> event = RelevantDate(
        ...     start_date="2026-03-15T17:00:00-08:00",  # 2 hours before
        ...     end_date="2026-03-15T21:00:00-08:00"     # End of event
        ... )
    """
    
    def __init__(self, date=None, start_date=None, end_date=None):
        """Initialize a new RelevantDate instance.
        
        Args:
            date (str, optional): Single date/time (ISO 8601) when pass becomes relevant.
                Use this OR start_date/end_date, not both.
            start_date (str, optional): Start of relevancy interval (ISO 8601).
                Requires end_date when specified.
            end_date (str, optional): End of relevancy interval (ISO 8601).
                Required when start_date is provided.
        
        Raises:
            ValueError: If both date and start_date/end_date are provided,
                or if start_date is provided without end_date, or vice versa.
        
        Note:
            Date format must be ISO 8601: YYYY-MM-DDTHH:MM:SS±HH:MM
            Dates must include hours and minutes, seconds are optional.
        """
        # Validation: can't mix 'date' with 'start_date/end_date'
        if date and (start_date or end_date):
            raise ValueError(
                "Cannot specify both 'date' and 'start_date/end_date'. "
                "Use 'date' for auto-calculated interval OR 'start_date/end_date' for explicit interval."
            )
        
        # Validation: start_date and end_date must be used together
        if (start_date and not end_date) or (end_date and not start_date):
            raise ValueError(
                "Both 'start_date' and 'end_date' must be provided together."
            )
        
        # At least one must be provided
        if not date and not start_date:
            raise ValueError(
                "Must provide either 'date' or both 'start_date' and 'end_date'."
            )
        
        self.date = date
        self.startDate = start_date  # Use camelCase for JSON compatibility
        self.endDate = end_date
    
    def json_dict(self):
        """Generate pass.json dictionary representation.
        
        Returns:
            dict: Dictionary with date fields, excluding None values.
        """
        result = {}
        
        if self.date:
            result["date"] = self.date
        
        if self.startDate:
            result["startDate"] = self.startDate
        
        if self.endDate:
            result["endDate"] = self.endDate
        
        return result
    
    def __repr__(self):
        """String representation for debugging.
        
        Returns:
            str: String representation of the RelevantDate.
        """
        if self.date:
            return f"RelevantDate(date='{self.date}')"
        else:
            return f"RelevantDate(start_date='{self.startDate}', end_date='{self.endDate}')"
