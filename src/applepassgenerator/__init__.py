__version__ = "0.0.2"
__author__ = "Primedigital Global"

# Models - Constants
from applepassgenerator.models.constants import (
    Alignment,
    BarcodeFormat,
    TransitType,
    DateStyle,
    NumberStyle,
    DataDetectorType,
    EventType,
    TransitStatus,
)

# Models - Fields
from applepassgenerator.models.fields import (
    Field,
    DateField,
    NumberField,
    CurrencyField,
)

# Models - Barcodes
from applepassgenerator.models.barcodes import Barcode

# Models - Locations
from applepassgenerator.models.locations import (
    Location,
    IBeacon,
)

# Models - Relevant Date
from applepassgenerator.models.relevant_date import RelevantDate

# Models - Semantic Tags
from applepassgenerator.models.semantic_tags import (
    SemanticTags,
    SemanticLocation,
    CurrencyAmount,
    Seat,
    PersonNameComponents,
    WifiNetwork,
)

# Models - Personalization
from applepassgenerator.models.personalization import (
    Personalization,
    PersonalizationField,
)

# Models - Pass Types
from applepassgenerator.models.pass_types import (
    PassInformation,
    BoardingPass,
    Coupon,
    EventTicket,
    Generic,
    StoreCard,
)

# Models - Pass Base
from applepassgenerator.models.pass_base import (
    ApplePass,
    pass_handler,
)

# Validators
from applepassgenerator.validators import (
    validate_rgb_color,
    validate_iso8601_date,
    validate_currency_code,
    validate_location_limits,
    validate_beacon_limits,
    validate_serial_number,
    validate_authentication_token,
)

# Utilities
from applepassgenerator.utils import (
    rgb_color,
    hex_to_rgb,
    format_iso8601,
)

# Client
from applepassgenerator.client import ApplePassGeneratorClient

# Backward compatibility alias
ApplePassClient = ApplePassGeneratorClient

# Define public API
__all__ = [
    # Version info
    "__version__",
    "__author__",
    # Constants
    "Alignment",
    "BarcodeFormat",
    "TransitType",
    "DateStyle",
    "NumberStyle",
    "DataDetectorType",
    "EventType",
    "TransitStatus",
    # Fields
    "Field",
    "DateField",
    "NumberField",
    "CurrencyField",
    # Barcodes
    "Barcode",
    # Relevant Date
    "RelevantDate", 
    # Locations
    "Location",
    "IBeacon",
    # Semantic Tags
    "SemanticTags",
    "SemanticLocation",
    "CurrencyAmount",
    "Seat",
    "PersonNameComponents",
    "WifiNetwork",
    # Personalization
    "Personalization",
    "PersonalizationField",
    # Pass Types
    "PassInformation",
    "BoardingPass",
    "Coupon",
    "EventTicket",
    "Generic",
    "StoreCard",
    # Pass Base
    "ApplePass",
    "pass_handler",
    # Validators
    "validate_rgb_color",
    "validate_iso8601_date",
    "validate_currency_code",
    "validate_location_limits",
    "validate_beacon_limits",
    "validate_serial_number",
    "validate_authentication_token",
    # Utilities
    "rgb_color",
    "hex_to_rgb",
    "format_iso8601",
    # Client
    "ApplePassGeneratorClient",
    "ApplePassClient",  # Backward compatibility alias
]
