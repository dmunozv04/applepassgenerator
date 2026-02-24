"""
Pass type classes for Apple Wallet passes.

This module contains the pass information classes that define the structure
and content of different pass types:
- PassInformation: Base class for all pass types
- BoardingPass: For airline, train, bus, and boat boarding passes
- Coupon: For coupons and promotional offers
- EventTicket: For event tickets (concerts, movies, sports, etc.)
- Generic: For generic passes (membership cards, loyalty cards, etc.)
- StoreCard: For retail store cards

All pass types support iOS 6.0+ features with progressive enhancement
for newer iOS versions up to iOS 18.0+.
"""

from typing import Any, Dict, List, Union

from .constants import TransitType
from .fields import Field


class PassInformation:
    """Base class for all pass type information.
    
    PassInformation is the abstract base class that defines the structure
    and field collections for all pass types in Apple Wallet. Each pass
    contains multiple field sections that organize information display:
    
    - Header Fields: Displayed at the top of the pass
    - Primary Fields: Most prominent information (large text)
    - Secondary Fields: Supporting information below primary
    - Auxiliary Fields: Additional details below secondary
    - Back Fields: Information shown on the back of the pass
    - Additional Info Fields (iOS 18.0+): For poster-style event tickets only
    
    iOS Version Support:
        - iOS 6.0+: header, primary, secondary, auxiliary, back fields
        - iOS 18.0+: additionalInfoFields (poster event tickets only)
    
    Attributes:
        header_fields (List[Field]): Fields displayed in the header section
        primary_fields (List[Field]): Primary (prominent) fields
        secondary_fields (List[Field]): Secondary information fields
        auxiliary_fields (List[Field]): Auxiliary information fields
        back_fields (List[Field]): Fields shown on the back of the pass
        additional_info_fields (List[Field]): iOS 18.0+ Additional info fields
            for poster-style event tickets
    
    Example:
        >>> pass_info = PassInformation()
        >>> pass_info.add_header_field("gate", "23", "Gate")
        >>> pass_info.add_primary_field("boardingTime", "3:45 PM", "Boarding Time")
        >>> pass_info.add_back_field("terms", "Terms and conditions...", "Terms")
    
    Notes:
        - This class should not be instantiated directly; use subclasses
        - Field keys must be unique within the pass
        - Not all field sections are required; use only what's needed
        - Additional info fields are only supported for EventTicket passes
          displayed in poster style (iOS 18.0+)
    """
    
    def __init__(self):
        """Initialize the PassInformation with empty field collections."""
        self.header_fields: List[Field] = []
        self.primary_fields: List[Field] = []
        self.secondary_fields: List[Field] = []
        self.back_fields: List[Field] = []
        self.auxiliary_fields: List[Field] = []
        self.additional_info_fields: List[Field] = []  # iOS 18.0+

    def add_header_field(
        self, 
        key: Union[str, Field], 
        value: Any = None, 
        label: str = ""
    ) -> Field:
        """Add a field to the header section (top of pass).
        
        Header fields appear at the top of the pass and are typically used
        for important identifying information like logos, names, or dates.
        
        Args:
            key: Either a Field object or a string key for the field
            value: The field's value (required if key is a string)
            label: Optional label text displayed above the value
        
        Returns:
            Field: The added field object (for chaining/modification)
        
        Example:
            >>> pass_info.add_header_field("date", "Oct 15", "Date")
            >>> # Or with a Field object:
            >>> field = Field("gate", "A23", "Gate")
            >>> pass_info.add_header_field(field)
        """
        field = Field(key, value, label) if isinstance(key, str) else key
        self.header_fields.append(field)
        return field

    def add_primary_field(
        self, 
        key: Union[str, Field], 
        value: Any = None, 
        label: str = ""
    ) -> Field:
        """Add a primary (prominent) field to the pass.
        
        Primary fields are displayed prominently with large text and are
        used for the most important information on the pass (e.g., balance
        on a store card, event name on a ticket).
        
        Args:
            key: Either a Field object or a string key for the field
            value: The field's value (required if key is a string)
            label: Optional label text displayed above the value
        
        Returns:
            Field: The added field object (for chaining/modification)
        
        Example:
            >>> pass_info.add_primary_field("balance", "$25.00", "Balance")
        """
        field = Field(key, value, label) if isinstance(key, str) else key
        self.primary_fields.append(field)
        return field

    def add_secondary_field(
        self, 
        key: Union[str, Field], 
        value: Any = None, 
        label: str = ""
    ) -> Field:
        """Add a secondary field to the pass.
        
        Secondary fields appear below primary fields and provide supporting
        information with medium-sized text.
        
        Args:
            key: Either a Field object or a string key for the field
            value: The field's value (required if key is a string)
            label: Optional label text displayed above the value
        
        Returns:
            Field: The added field object (for chaining/modification)
        
        Example:
            >>> pass_info.add_secondary_field("venue", "Madison Square Garden", "Venue")
        """
        field = Field(key, value, label) if isinstance(key, str) else key
        self.secondary_fields.append(field)
        return field

    def add_back_field(
        self, 
        key: Union[str, Field], 
        value: Any = None, 
        label: str = ""
    ) -> Field:
        """Add a field to the back of the pass.
        
        Back fields are shown when the user flips the pass over and are
        typically used for detailed information, terms and conditions,
        or contact details.
        
        Args:
            key: Either a Field object or a string key for the field
            value: The field's value (required if key is a string)
            label: Optional label text displayed above the value
        
        Returns:
            Field: The added field object (for chaining/modification)
        
        Example:
            >>> pass_info.add_back_field("terms", "Terms apply...", "Terms & Conditions")
        """
        field = Field(key, value, label) if isinstance(key, str) else key
        self.back_fields.append(field)
        return field

    def add_auxiliary_field(
        self, 
        key: Union[str, Field], 
        value: Any = None, 
        label: str = ""
    ) -> Field:
        """Add an auxiliary field to the pass.
        
        Auxiliary fields appear below secondary fields and provide
        additional supporting information with smaller text.
        
        Args:
            key: Either a Field object or a string key for the field
            value: The field's value (required if key is a string)
            label: Optional label text displayed above the value
        
        Returns:
            Field: The added field object (for chaining/modification)
        
        Example:
            >>> pass_info.add_auxiliary_field("section", "101", "Section")
        """
        field = Field(key, value, label) if isinstance(key, str) else key
        self.auxiliary_fields.append(field)
        return field
    
    def add_additional_info_field(
        self, 
        key: Union[str, Field], 
        value: Any = None, 
        label: str = ""
    ) -> Field:
        """Add an additional info field (iOS 18.0+, poster event tickets only).
        
        Additional info fields are only supported for EventTicket passes
        displayed in poster style on iOS 18.0+. They provide supplementary
        information displayed at the bottom of the poster-style ticket.
        
        iOS Version: 18.0+
        
        Args:
            key: Either a Field object or a string key for the field
            value: The field's value (required if key is a string)
            label: Optional label text displayed above the value
        
        Returns:
            Field: The added field object (for chaining/modification)
        
        Example:
            >>> event_ticket = EventTicket()
            >>> event_ticket.add_additional_info_field(
            ...     "parking", "Lot A", "Parking Information"
            ... )
        
        Notes:
            - Only available for EventTicket passes in poster style
            - Requires iOS 18.0+ to display
            - Will be ignored on older iOS versions
            - Should not be used with other pass types
        """
        field = Field(key, value, label) if isinstance(key, str) else key
        self.additional_info_fields.append(field)
        return field

    def json_dict(self) -> Dict[str, Any]:
        """Serialize the pass information to a dictionary for JSON export.
        
        Creates a dictionary containing all non-empty field sections in the
        format required by Apple Wallet's pass.json specification.
        
        Returns:
            Dict[str, Any]: Dictionary with field sections (headerFields,
                primaryFields, secondaryFields, auxiliaryFields, backFields,
                and optionally additionalInfoFields for iOS 18.0+)
        
        Notes:
            - Empty field sections are omitted from the output
            - Each field is serialized using its json_dict() method
            - Field keys use camelCase as per Apple's specification
        """
        d: Dict[str, Any] = {}
        
        if self.header_fields:
            d["headerFields"] = [f.json_dict() for f in self.header_fields]
        if self.primary_fields:
            d["primaryFields"] = [f.json_dict() for f in self.primary_fields]
        if self.secondary_fields:
            d["secondaryFields"] = [f.json_dict() for f in self.secondary_fields]
        if self.back_fields:
            d["backFields"] = [f.json_dict() for f in self.back_fields]
        if self.auxiliary_fields:
            d["auxiliaryFields"] = [f.json_dict() for f in self.auxiliary_fields]
        if self.additional_info_fields:
            d["additionalInfoFields"] = [f.json_dict() for f in self.additional_info_fields]
        
        return d


class BoardingPass(PassInformation):
    """Boarding pass for air, train, bus, boat, or generic transit.
    
    The BoardingPass class represents travel boarding passes for various
    transit types (airplane, train, bus, boat, etc.). It extends
    PassInformation with transit-type-specific functionality.
    
    iOS Version Support:
        - iOS 6.0+: All transit types and features
    
    Attributes:
        transit_type (str): Type of transit (use TransitType constants)
        jsonname (str): JSON key for this pass type ("boardingPass")
    
    Example:
        >>> from applepassgenerator.models import BoardingPass, TransitType
        >>> boarding_pass = BoardingPass(TransitType.AIR)
        >>> boarding_pass.add_primary_field("origin", "SFO", "San Francisco")
        >>> boarding_pass.add_primary_field("destination", "LAX", "Los Angeles")
        >>> boarding_pass.add_secondary_field("gate", "A23", "Gate")
        >>> boarding_pass.add_secondary_field("seat", "12F", "Seat")
    
    Notes:
        - Barcode can contain ticket confirmation number
        - Logo is typically airline/transit company logo
        - Strip image often shows route map or scenic view
        - Background image can show aircraft/train exterior
    """
    
    def __init__(self, transit_type: str = TransitType.AIR):
        """Initialize a BoardingPass with the specified transit type.
        
        Args:
            transit_type: Type of transit (default: TransitType.AIR)
                Use TransitType constants: AIR, TRAIN, BUS, BOAT, GENERIC
        
        Example:
            >>> boarding_pass = BoardingPass(TransitType.TRAIN)
        """
        super().__init__()
        self.transit_type = transit_type
        self.jsonname = "boardingPass"
    
    @property
    def transit_type(self) -> str:
        """Get the transit type for this boarding pass.
        
        Returns:
            str: The transit type (e.g., "PKTransitTypeAir")
        """
        return self._transit_type
    
    @transit_type.setter
    def transit_type(self, value: str) -> None:
        """Set the transit type for this boarding pass.
        
        Args:
            value: Transit type value (use TransitType constants)
        """
        self._transit_type = value

    def json_dict(self) -> Dict[str, Any]:
        """Serialize the boarding pass to a dictionary for JSON export.
        
        Returns:
            Dict[str, Any]: Dictionary containing all fields and transitType
        """
        d = super().json_dict()
        d["transitType"] = self.transit_type
        return d


class Coupon(PassInformation):
    """Coupon pass for promotional offers and discounts.
    
    The Coupon class represents promotional coupons, discount offers,
    and special deals. Coupons typically include an offer description,
    expiration date, and barcode for redemption.
    
    iOS Version Support:
        - iOS 6.0+
    
    Attributes:
        jsonname (str): JSON key for this pass type ("coupon")
    
    Example:
        >>> from applepassgenerator.models import Coupon
        >>> coupon = Coupon()
        >>> coupon.add_primary_field("offer", "50% OFF", "Special Offer")
        >>> coupon.add_secondary_field("expires", "Dec 31, 2026", "Expires")
        >>> coupon.add_back_field(
        ...     "terms", 
        ...     "Valid on regular priced items only...", 
        ...     "Terms & Conditions"
        ... )
    
    Notes:
        - Primary field typically contains the offer/discount
        - Barcode used for scanning at point of sale
        - Logo image shows merchant logo
        - Strip image can show promotional graphics
        - Set expiration_date on ApplePass to auto-archive expired coupons
    """
    
    def __init__(self):
        """Initialize a Coupon pass."""
        super().__init__()
        self.jsonname = "coupon"


class EventTicket(PassInformation):
    """Event ticket for concerts, movies, sports, and other events.
    
    The EventTicket class represents tickets for various events including
    concerts, movies, sports games, theater performances, and conferences.
    
    iOS Version Support:
        - iOS 6.0+: Basic event ticket support
        - iOS 12.0+: Semantic tags for structured event information
        - iOS 18.0+: Poster-style display with additionalInfoFields
    
    Attributes:
        jsonname (str): JSON key for this pass type ("eventTicket")
    
    Example:
        >>> from applepassgenerator.models import EventTicket
        >>> ticket = EventTicket()
        >>> ticket.add_header_field("eventName", "Rock Concert", "Event")
        >>> ticket.add_primary_field("section", "A", "Section")
        >>> ticket.add_secondary_field("seat", "12", "Seat")
        >>> ticket.add_auxiliary_field("doors", "7:00 PM", "Doors Open")
        >>> ticket.add_back_field("venue_info", "123 Main St...", "Venue")
        >>> 
        >>> # iOS 18.0+: Add additional info for poster-style tickets
        >>> ticket.add_additional_info_field("parking", "Lot B", "Parking")
    
    Notes:
        - Logo typically shows event or venue logo
        - Strip/thumbnail image can show performer or event image
        - Background can be event-themed artwork
        - Use semantic tags (iOS 12.0+) for enhanced functionality
        - Poster-style display (iOS 18.0+) provides larger, more immersive view
        - Additional info fields only appear in poster style (iOS 18.0+)
    """
    
    def __init__(self):
        """Initialize an EventTicket pass."""
        super().__init__()
        self.jsonname = "eventTicket"


class Generic(PassInformation):
    """Generic pass for general-purpose cards and tickets.
    
    The Generic class represents general-purpose passes that don't fit
    into other specific categories. Common uses include gym memberships,
    loyalty cards, ID cards, library cards, and gift certificates.
    
    iOS Version Support:
        - iOS 6.0+
    
    Attributes:
        jsonname (str): JSON key for this pass type ("generic")
    
    Example:
        >>> from applepassgenerator.models import Generic
        >>> generic = Generic()
        >>> generic.add_header_field("company", "Acme Gym", "")
        >>> generic.add_primary_field("member", "John Doe", "Member Name")
        >>> generic.add_secondary_field("memberID", "123456", "Member ID")
        >>> generic.add_auxiliary_field("since", "Jan 2023", "Member Since")
        >>> generic.add_back_field(
        ...     "benefits", 
        ...     "Full access to all facilities...", 
        ...     "Membership Benefits"
        ... )
    
    Notes:
        - Most flexible pass type with no specific layout requirements
        - Logo shows organization/company logo
        - Thumbnail image can show member photo or org logo
        - Strip image can display branding or decorative graphics
        - Suitable for any use case not covered by other pass types
    """
    
    def __init__(self):
        """Initialize a Generic pass."""
        super().__init__()
        self.jsonname = "generic"


class StoreCard(PassInformation):
    """Store card for retail loyalty and rewards programs.
    
    The StoreCard class represents retail store cards, loyalty programs,
    and rewards cards. These passes typically display current balance,
    points, or rewards status.
    
    iOS Version Support:
        - iOS 6.0+
    
    Attributes:
        jsonname (str): JSON key for this pass type ("storeCard")
    
    Example:
        >>> from applepassgenerator.models import StoreCard
        >>> store_card = StoreCard()
        >>> store_card.add_header_field("store", "Coffee Shop", "")
        >>> store_card.add_primary_field("balance", "$25.00", "Balance")
        >>> store_card.add_secondary_field("rewards", "125", "Rewards Points")
        >>> store_card.add_auxiliary_field("member", "Gold", "Member Level")
        >>> store_card.add_back_field(
        ...     "contact",
        ...     "Visit coffeshop.com or call 555-0100",
        ...     "Contact Us"
        ... )
    
    Notes:
        - Primary field typically shows balance or points
        - Logo displays store/brand logo
        - Strip image can show promotional content
        - Barcode used for scanning at checkout
        - Can include web service for real-time balance updates
        - Use locations for relevance at store locations
    """
    
    def __init__(self):
        """Initialize a StoreCard pass."""
        super().__init__()
        self.jsonname = "storeCard"
