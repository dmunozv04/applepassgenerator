"""Semantic tags for Apple Wallet Passes.

iOS 12.0+

Machine-readable metadata that enables system suggestions and enhanced functionality.
Can be placed at pass level or field level.
"""


class SemanticLocation:
    """Location for semantic tags.
    
    iOS 12.0+
    
    Attributes:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
    """
    
    def __init__(self, latitude, longitude):
        """Initialize a semantic location.
        
        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
        """
        self.latitude = float(latitude)
        self.longitude = float(longitude)
    
    def json_dict(self):
        """Convert to JSON dictionary.
        
        Returns:
            dict: JSON representation of the location
        """
        return {"latitude": self.latitude, "longitude": self.longitude}


class CurrencyAmount:
    """Currency amount for semantic tags.
    
    iOS 14.0+
    
    Attributes:
        amount (str): Numeric amount as string
        currencyCode (str): ISO 4217 currency code (e.g., "USD", "EUR")
    """
    
    def __init__(self, amount, currency_code):
        """Initialize a currency amount.
        
        Args:
            amount (str/float): Numeric amount
            currency_code (str): ISO 4217 currency code (e.g., "USD")
        """
        self.amount = str(amount)
        self.currencyCode = currency_code
    
    def json_dict(self):
        """Convert to JSON dictionary.
        
        Returns:
            dict: JSON representation of the currency amount
        """
        return {"amount": self.amount, "currencyCode": self.currencyCode}


class Seat:
    """Seat information for semantic tags.
    
    iOS 12.0+
    
    Attributes:
        seatSection (str): Seat section identifier
        seatRow (str): Seat row identifier
        seatNumber (str): Seat number
        seatIdentifier (str): Unique seat identifier
        seatType (str): Type of seat
        seatDescription (str): Description of the seat
    """
    
    def __init__(self):
        """Initialize a seat with all optional fields."""
        self.seatSection = None
        self.seatRow = None
        self.seatNumber = None
        self.seatIdentifier = None
        self.seatType = None
        self.seatDescription = None
    
    def json_dict(self):
        """Convert to JSON dictionary.
        
        Returns:
            dict: JSON representation with non-None values only
        """
        d = {}
        for key, value in self.__dict__.items():
            if value is not None:
                d[key] = value
        return d


class PersonNameComponents:
    """Person name components for semantic tags.
    
    iOS 12.0+
    
    Attributes:
        givenName (str): Given name (first name)
        familyName (str): Family name (last name)
        middleName (str): Middle name
        namePrefix (str): Name prefix (e.g., "Dr.", "Mr.")
        nameSuffix (str): Name suffix (e.g., "Jr.", "III")
        nickname (str): Nickname
        phoneticRepresentation (str): Phonetic representation
    """
    
    def __init__(self):
        """Initialize person name components with all optional fields."""
        self.givenName = None
        self.familyName = None
        self.middleName = None
        self.namePrefix = None
        self.nameSuffix = None
        self.nickname = None
        self.phoneticRepresentation = None
    
    def json_dict(self):
        """Convert to JSON dictionary.
        
        Returns:
            dict: JSON representation with non-None values only
        """
        d = {}
        for key, value in self.__dict__.items():
            if value is not None:
                d[key] = value
        return d


class WifiNetwork:
    """WiFi network information for semantic tags.
    
    iOS 12.0+
    
    Attributes:
        ssid (str): Network SSID (required)
        password (str): Network password (required)
    """
    
    def __init__(self, ssid, password):
        """Initialize WiFi network information.
        
        Args:
            ssid (str): Network SSID
            password (str): Network password
        """
        self.ssid = ssid
        self.password = password
    
    def json_dict(self):
        """Convert to JSON dictionary.
        
        Returns:
            dict: JSON representation of the WiFi network
        """
        return {"ssid": self.ssid, "password": self.password}


class SemanticTags:
    """Machine-readable metadata for passes.
    
    iOS 12.0+
    
    Can be placed at pass level or field level.
    Enables system suggestions and enhanced functionality such as:
    - Do Not Disturb suggestions for events
    - Lock screen pass display based on time/location
    - Siri suggestions
    - Calendar integration
    
    All properties are optional (default None).
    
    Event Information:
        eventType (str): Event type constant (e.g., EventType.MOVIE)
        eventName (str): Name of the event
        eventStartDate (str): ISO 8601 date string
        eventEndDate (str): ISO 8601 date string
        eventDuration (float): Duration in seconds (iOS 18.0+)
        silenceRequested (bool): Request Do Not Disturb mode
    
    Venue Information:
        venueName (str): Name of the venue
        venueLocation (SemanticLocation): Location of the venue
        venueEntrance (str): Entrance identifier
        venuePhoneNumber (str): Venue phone number
        venueRoom (str): Room identifier
    
    Seating:
        seats (list[Seat]): List of Seat objects
    
    Sports:
        leagueName (str): Name of the sports league
        leagueAbbreviation (str): League abbreviation
        homeTeamLocation (str): Home team location
        homeTeamName (str): Home team name
        homeTeamAbbreviation (str): Home team abbreviation
        awayTeamLocation (str): Away team location
        awayTeamName (str): Away team name
        awayTeamAbbreviation (str): Away team abbreviation
        sportName (str): Name of the sport
    
    Performance:
        genre (str): Performance genre
        performerNames (list[str]): List of performer names
        artistIDs (list[str]): List of artist identifiers
    
    Airline/Transit:
        airlineCode (str): IATA airline code
        flightCode (str): Flight code
        flightNumber (int): Flight number
        transitProvider (str): Transit provider name
        transitStatus (str): Transit status
        transitStatusReason (str): Reason for transit status
        vehicleName (str): Vehicle name
        vehicleType (str): Vehicle type
        vehicleNumber (str): Vehicle number
        departureLocation (SemanticLocation): Departure location
        departurePlatform (str): Departure platform
        departureGate (str): Departure gate
        departureTerminal (str): Departure terminal
        destinationLocation (SemanticLocation): Destination location
        destinationPlatform (str): Destination platform
        destinationGate (str): Destination gate
        destinationTerminal (str): Destination terminal
        arrivalGate (str): Arrival gate (iOS 18.0+)
        arrivalPlatform (str): Arrival platform (iOS 18.0+)
        arrivalTerminal (str): Arrival terminal (iOS 18.0+)
        originStationName (str): Origin station name
        originStationCode (str): Origin station code
        destinationStationName (str): Destination station name
        destinationStationCode (str): Destination station code
        boardingGroup (str): Boarding group
        boardingSequenceNumber (str): Boarding sequence number
        confirmationNumber (str): Confirmation number
        passengerName (PersonNameComponents): Passenger name components
        membershipProgramName (str): Membership program name
        membershipProgramNumber (str): Membership program number
        priorityStatus (str): Priority status
        securityScreening (str): Security screening information
        carNumber (str): Car number
        originalDepartureDate (str): Original departure date (ISO 8601)
        originalArrivalDate (str): Original arrival date (ISO 8601)
        originalBoardingDate (str): Original boarding date (ISO 8601)
        currentDepartureDate (str): Current departure date (ISO 8601)
        currentArrivalDate (str): Current arrival date (ISO 8601)
        currentBoardingDate (str): Current boarding date (ISO 8601)
    
    Currency (iOS 14.0+):
        balance (CurrencyAmount): Balance amount
        totalPrice (CurrencyAmount): Total price amount
    
    WiFi:
        wifiAccess (list[WifiNetwork]): List of WiFi networks
    
    Other:
        duration (float): Duration in seconds
    """
    
    def __init__(self):
        """Initialize semantic tags with all optional fields set to None."""
        # Event Information
        self.eventType = None
        self.eventName = None
        self.eventStartDate = None
        self.eventEndDate = None
        self.eventDuration = None  # iOS 18.0+
        self.silenceRequested = None
        
        # Venue
        self.venueName = None
        self.venueLocation = None  # SemanticLocation object
        self.venueEntrance = None
        self.venuePhoneNumber = None
        self.venueRoom = None
        
        # Seating
        self.seats = None  # List of Seat objects
        
        # Sports
        self.homeTeamAbbreviation = None
        self.homeTeamLocation = None
        self.homeTeamName = None
        self.awayTeamAbbreviation = None
        self.awayTeamLocation = None
        self.awayTeamName = None
        self.sportName = None
        self.leagueName = None
        self.leagueAbbreviation = None
        
        # Performance
        self.genre = None
        self.performerNames = None  # List of strings
        self.artistIDs = None  # List of strings
        
        # Transit/Boarding
        self.transitProvider = None
        self.vehicleName = None
        self.vehicleType = None
        self.vehicleNumber = None
        self.originStationName = None
        self.originStationCode = None
        self.destinationStationName = None
        self.destinationStationCode = None
        self.transitStatus = None
        self.transitStatusReason = None
        self.boardingGroup = None
        self.boardingSequenceNumber = None
        self.confirmationNumber = None
        self.departureLocation = None  # SemanticLocation
        self.destinationLocation = None  # SemanticLocation
        self.departureGate = None
        self.departurePlatform = None
        self.departureTerminal = None
        self.destinationGate = None
        self.destinationPlatform = None
        self.destinationTerminal = None
        self.arrivalGate = None  # iOS 18.0+
        self.arrivalPlatform = None  # iOS 18.0+
        self.arrivalTerminal = None  # iOS 18.0+
        self.securityScreening = None
        self.carNumber = None
        self.airlineCode = None
        self.flightCode = None
        self.flightNumber = None  # Number
        self.originalDepartureDate = None
        self.originalArrivalDate = None
        self.originalBoardingDate = None
        self.currentDepartureDate = None
        self.currentArrivalDate = None
        self.currentBoardingDate = None
        
        # Balance & Currency (iOS 14.0+)
        self.balance = None  # CurrencyAmount object
        self.totalPrice = None  # CurrencyAmount object
        
        # WiFi
        self.wifiAccess = None  # List of WifiNetwork objects
        
        # Membership
        self.membershipProgramName = None
        self.membershipProgramNumber = None
        self.priorityStatus = None
        self.passengerName = None  # PersonNameComponents object

    def json_dict(self):
        """Generate JSON dictionary, excluding None values and converting objects.
        
        Returns:
            dict: JSON representation with non-None values only
        """
        d = {}
        for key, value in self.__dict__.items():
            if value is not None:
                # Handle objects with json_dict method
                if hasattr(value, 'json_dict'):
                    d[key] = value.json_dict()
                # Handle lists of objects
                elif isinstance(value, list):
                    if value and hasattr(value[0], 'json_dict'):
                        d[key] = [item.json_dict() for item in value]
                    else:
                        d[key] = value
                else:
                    d[key] = value
        return d
