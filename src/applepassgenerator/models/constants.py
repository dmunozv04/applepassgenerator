"""
Constants and enums for Apple Wallet Pass fields.

This module contains all the constant values used throughout the library
for pass field alignment, barcode formats, transit types, date/number styles,
and semantic tag values.
"""


class Alignment:
    """Text alignment options for pass fields.
    
    iOS 6.0+
    """
    LEFT = "PKTextAlignmentLeft"
    CENTER = "PKTextAlignmentCenter"
    RIGHT = "PKTextAlignmentRight"
    JUSTIFIED = "PKTextAlignmentJustified"
    NATURAL = "PKTextAlignmentNatural"


class BarcodeFormat:
    """Barcode format types supported by Apple Wallet.
    
    iOS 6.0+ (PDF417, QR, AZTEC)
    iOS 9.0+ (CODE128)
    """
    PDF417 = "PKBarcodeFormatPDF417"
    QR = "PKBarcodeFormatQR"
    AZTEC = "PKBarcodeFormatAztec"
    CODE128 = "PKBarcodeFormatCode128"


class TransitType:
    """Transit type values for boarding passes.
    
    iOS 6.0+
    """
    AIR = "PKTransitTypeAir"
    TRAIN = "PKTransitTypeTrain"
    BUS = "PKTransitTypeBus"
    BOAT = "PKTransitTypeBoat"
    GENERIC = "PKTransitTypeGeneric"


class DateStyle:
    """Date and time display style options.
    
    iOS 6.0+
    """
    NONE = "PKDateStyleNone"
    SHORT = "PKDateStyleShort"
    MEDIUM = "PKDateStyleMedium"
    LONG = "PKDateStyleLong"
    FULL = "PKDateStyleFull"


class NumberStyle:
    """Number formatting style options.
    
    iOS 6.0+
    """
    DECIMAL = "PKNumberStyleDecimal"
    PERCENT = "PKNumberStylePercent"
    SCIENTIFIC = "PKNumberStyleScientific"
    SPELLOUT = "PKNumberStyleSpellOut"


class DataDetectorType:
    """Data detector types for automatic link detection in pass fields.
    
    iOS 10.0+
    """
    PHONE_NUMBER = "PKDataDetectorTypePhoneNumber"
    LINK = "PKDataDetectorTypeLink"
    ADDRESS = "PKDataDetectorTypeAddress"
    CALENDAR_EVENT = "PKDataDetectorTypeCalendarEvent"


class EventType:
    """Event types for semantic tags.
    
    iOS 12.0+
    """
    GENERIC = "PKEventTypeGeneric"
    LIVE_PERFORMANCE = "PKEventTypeLivePerformance"
    MOVIE = "PKEventTypeMovie"
    SPORTS = "PKEventTypeSports"
    CONFERENCE = "PKEventTypeConference"
    CONVENTION = "PKEventTypeConvention"
    WORKSHOP = "PKEventTypeWorkshop"
    SOCIAL_GATHERING = "PKEventTypeSocialGathering"


class TransitStatus:
    """Transit status values for boarding passes with semantic tags.
    
    iOS 12.0+
    """
    SCHEDULED = "PKTransitStatusScheduled"
    DELAYED = "PKTransitStatusDelayed"
    CANCELLED = "PKTransitStatusCancelled"
    BOARDING = "PKTransitStatusBoarding"
    ARRIVED = "PKTransitStatusArrived"
