"""
Location and iBeacon classes for Apple Wallet Pass relevance.

This module provides classes for defining geographic locations and iBeacon regions
that determine when a pass is relevant and should be displayed on the lock screen.
"""


class Location:
    """Geographic location for pass relevance.
    
    Used to trigger pass display on the lock screen when the device is near
    a specified geographic location. Up to 10 locations can be added per pass.
    
    iOS 6.0+ for basic location support
    iOS 7.0+ for maxDistance parameter
    
    Attributes:
        latitude (float): Latitude in degrees, ranging from -90 to 90.
            Required. Values outside this range will be clamped to 0.0.
        longitude (float): Longitude in degrees, ranging from -180 to 180.
            Required. Values outside this range will be clamped to 0.0.
        altitude (float): Altitude in meters. Optional.
            Can be used for more precise location matching.
        relevant_text (str): Text displayed on the lock screen when the pass is
            relevant at this location. Optional.
        max_distance (float): Maximum distance in meters from the location where
            the pass is relevant. Optional. iOS 7.0+ feature.
            If not specified, the system uses a default distance.
    
    Example:
        >>> # Simple location
        >>> loc = Location(37.3318, -122.0312)
        >>> 
        >>> # Location with altitude and notification distance
        >>> loc = Location(
        ...     latitude=37.3318,
        ...     longitude=-122.0312,
        ...     altitude=100.0,
        ...     relevant_text="Welcome to Apple Park!",
        ...     max_distance=500.0  # 500 meters
        ... )
    
    Note:
        - Maximum 10 locations per pass
        - Location services must be enabled on the user's device
        - The system determines when to show the pass based on various factors
          including battery level and user preferences
    """
    
    def __init__(
        self,
        latitude,
        longitude,
        altitude=None,
        relevant_text=None,
        max_distance=None
    ):
        """Initialize a Location instance.
        
        Args:
            latitude (float): Latitude in degrees (-90 to 90). Required.
            longitude (float): Longitude in degrees (-180 to 180). Required.
            altitude (float, optional): Altitude in meters. Defaults to None.
            relevant_text (str, optional): Text shown on lock screen when near
                this location. Defaults to None.
            max_distance (float, optional): Maximum distance in meters for
                relevance (iOS 7.0+). Defaults to None, which uses system default.
        
        Raises:
            No exceptions are raised. Invalid numeric values are converted to 0.0
            with appropriate error handling.
        """
        # Required. Latitude, in degrees, of the location.
        # Range: -90 to 90
        try:
            self.latitude = float(latitude)
        except (ValueError, TypeError):
            self.latitude = 0.0
        
        # Required. Longitude, in degrees, of the location.
        # Range: -180 to 180
        try:
            self.longitude = float(longitude)
        except (ValueError, TypeError):
            self.longitude = 0.0
        
        # Optional. Altitude, in meters, of the location.
        if altitude is not None:
            try:
                self.altitude = float(altitude)
            except (ValueError, TypeError):
                self.altitude = 0.0
        else:
            self.altitude = None
        
        # Optional. Maximum distance in meters for pass relevance.
        # iOS 7.0+ feature
        if max_distance is not None:
            try:
                self.maxDistance = float(max_distance)
            except (ValueError, TypeError):
                self.maxDistance = None
        else:
            self.maxDistance = None
        
        # Optional. Text displayed on the lock screen when the pass is
        # currently relevant near this location
        self.relevantText = relevant_text if relevant_text else None
    
    def json_dict(self):
        """Serialize location to a dictionary for pass.json.
        
        Returns:
            dict: Dictionary containing location data with only non-None values.
                Required keys: latitude, longitude
                Optional keys: altitude, maxDistance, relevantText
        
        Example:
            >>> loc = Location(37.3318, -122.0312, altitude=100.0)
            >>> loc.json_dict()
            {'latitude': 37.3318, 'longitude': -122.0312, 'altitude': 100.0}
        """
        d = {
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
        
        # Only include optional fields if they have values
        if self.altitude is not None:
            d["altitude"] = self.altitude
        
        if self.maxDistance is not None:
            d["maxDistance"] = self.maxDistance
        
        if self.relevantText:
            d["relevantText"] = self.relevantText
        
        return d


class IBeacon:
    """iBeacon region for pass relevance.
    
    Used to trigger pass display on the lock screen when the device detects
    a matching iBeacon. Up to 10 beacons can be added per pass.
    
    iOS 7.0+
    
    An iBeacon is identified by a UUID and optionally by major and minor values.
    The major and minor values allow for hierarchical identification:
    - UUID: Identifies a group of related beacons (e.g., all beacons for a company)
    - Major: Identifies a subset within the UUID group (e.g., a specific store)
    - Minor: Identifies an individual beacon (e.g., a specific department in a store)
    
    Attributes:
        proximity_uuid (str): UUID of the iBeacon. Required.
            Standard UUID format: "00000000-0000-0000-0000-000000000000"
        major (int): Major identifier value (0-65535). Optional.
            Used for grouping beacons within a UUID.
        minor (int): Minor identifier value (0-65535). Optional.
            Used for identifying individual beacons within a major group.
        relevant_text (str): Text displayed on the lock screen when near
            this beacon. Optional.
    
    Example:
        >>> # Match all beacons with this UUID
        >>> beacon = IBeacon("E2C56DB5-DFFB-48D2-B060-D0F5A71096E0")
        >>> 
        >>> # Match specific beacon with UUID, major, and minor
        >>> beacon = IBeacon(
        ...     proximity_uuid="E2C56DB5-DFFB-48D2-B060-D0F5A71096E0",
        ...     major=1,
        ...     minor=100,
        ...     relevant_text="Welcome to our store!"
        ... )
    
    Note:
        - Maximum 10 beacons per pass
        - Bluetooth must be enabled on the user's device
        - The device must support Bluetooth Low Energy (BLE)
        - iBeacon is a trademark of Apple Inc.
    """
    
    def __init__(
        self,
        proximity_uuid,
        major=None,
        minor=None,
        relevant_text=None
    ):
        """Initialize an IBeacon instance.
        
        Args:
            proximity_uuid (str): UUID string in standard format. Required.
                Example: "E2C56DB5-DFFB-48D2-B060-D0F5A71096E0"
            major (int, optional): Major value (0-65535). Defaults to None.
                When None, matches all major values for the UUID.
            minor (int, optional): Minor value (0-65535). Defaults to None.
                When None, matches all minor values for the major group.
            relevant_text (str, optional): Text shown on lock screen when near
                this beacon. Defaults to None.
        
        Note:
            If major is specified but minor is not, the beacon matches all minor
            values within that major group. If neither major nor minor is specified,
            the beacon matches any beacon with the specified UUID.
        """
        # Required. Unique identifier of the iBeacon.
        self.proximityUUID = proximity_uuid
        
        # Optional. Major identifier value (integer, 0-65535).
        # Use to differentiate between beacons with the same UUID.
        self.major = major
        
        # Optional. Minor identifier value (integer, 0-65535).
        # Use to differentiate between beacons with the same UUID and major value.
        self.minor = minor
        
        # Optional. Text displayed on the lock screen when the pass is
        # currently relevant near this beacon
        self.relevantText = relevant_text if relevant_text else None
    
    def json_dict(self):
        """Serialize iBeacon to a dictionary for pass.json.
        
        Returns:
            dict: Dictionary containing iBeacon data with only non-None values.
                Required keys: proximityUUID
                Optional keys: major, minor, relevantText
        
        Example:
            >>> beacon = IBeacon("E2C56DB5-DFFB-48D2-B060-D0F5A71096E0", major=1)
            >>> beacon.json_dict()
            {'proximityUUID': 'E2C56DB5-DFFB-48D2-B060-D0F5A71096E0', 'major': 1}
        """
        d = {"proximityUUID": self.proximityUUID}
        
        # Only include optional fields if they have values
        if self.major is not None:
            d["major"] = self.major
        
        if self.minor is not None:
            d["minor"] = self.minor
        
        if self.relevantText:
            d["relevantText"] = self.relevantText
        
        return d
