"""
Barcode classes for Apple Wallet passes.

This module provides the Barcode class for representing barcode information
in Apple Wallet passes, supporting multiple barcode formats.
"""

from .constants import BarcodeFormat


class Barcode:
    """Barcode representation for Apple Wallet passes.
    
    Supports encoding pass data in various barcode formats for scanning and
    identification purposes. Multiple barcodes can be added to a pass to support
    different devices and use cases.
    
    iOS 6.0+: Initial barcode support (singular 'barcode' field)
    iOS 9.0+: Multiple barcodes support ('barcodes' array) - RECOMMENDED
    
    Supported Barcode Formats:
        - PDF417: High-capacity 2D barcode (iOS 6.0+)
        - QR: Quick Response code (iOS 6.0+)
        - AZTEC: Compact 2D barcode (iOS 6.0+)
        - CODE128: Linear barcode for alphanumeric data (iOS 9.0+)
    
    Note:
        The singular 'barcode' field was deprecated in iOS 9.0 in favor of the
        'barcodes' array to support multiple barcode formats. This implementation
        supports the modern 'barcodes' array approach. The library automatically
        generates legacy 'barcode' field for backward compatibility with older iOS
        versions.
    
    Examples:
        >>> # Create a PDF417 barcode (default)
        >>> barcode = Barcode("PASS-12345-ABCDE")
        
        >>> # Create a QR code with custom encoding
        >>> qr_barcode = Barcode(
        ...     message="https://example.com/pass/12345",
        ...     format=BarcodeFormat.QR,
        ...     encoding="utf-8"
        ... )
        
        >>> # Create a barcode with alternative text
        >>> barcode = Barcode(
        ...     message="1234567890",
        ...     format=BarcodeFormat.CODE128,
        ...     alt_text="Membership: 1234567890"
        ... )
    """
    
    def __init__(
        self,
        message,
        format=BarcodeFormat.PDF417,
        encoding="iso-8859-1",
        alt_text=None
    ):
        """Initialize a new Barcode instance.
        
        Args:
            message (str): The message or payload to be encoded in the barcode.
                This is the data that will be scanned. Required.
            format (str, optional): The barcode format to use. Must be one of the
                BarcodeFormat constants (PDF417, QR, AZTEC, CODE128).
                Defaults to BarcodeFormat.PDF417 for backward compatibility.
            encoding (str, optional): Text encoding for converting the message.
                Common values: "iso-8859-1" (default), "utf-8", "windows-1252".
                Must be a valid IANA character set name. Defaults to "iso-8859-1".
            alt_text (str, optional): Text displayed near the barcode when space
                is available. Typically used to show a human-readable version of
                the barcode message. Defaults to None.
        
        Attributes:
            message (str): The barcode message/payload.
            format (str): The barcode format (PKBarcodeFormat* constant).
            messageEncoding (str): The character encoding for the message.
            altText (str): Optional alternative text displayed with the barcode.
        
        Examples:
            >>> # Simple barcode with default settings
            >>> barcode = Barcode("TICKET-789456")
            
            >>> # QR code with UTF-8 encoding for Unicode support
            >>> barcode = Barcode(
            ...     message="会員番号: 12345",
            ...     format=BarcodeFormat.QR,
            ...     encoding="utf-8"
            ... )
            
            >>> # Aztec barcode with alternative text
            >>> barcode = Barcode(
            ...     message="ABC123XYZ",
            ...     format=BarcodeFormat.AZTEC,
            ...     alt_text="Confirmation: ABC123XYZ"
            ... )
        """
        self.format = format
        self.message = message
        self.messageEncoding = encoding
        
        if alt_text is not None:
            self.altText = alt_text
    
    @property
    def message(self):
        """Get the barcode message/payload.
        
        Returns:
            str: The message encoded in the barcode.
        """
        return self._message
    
    @message.setter
    def message(self, value):
        """Set the barcode message/payload.
        
        Args:
            value (str): The message to encode in the barcode.
        
        Raises:
            ValueError: If message is None or empty.
        """
        if not value:
            raise ValueError("Barcode message cannot be empty")
        self._message = value
    
    @property
    def format(self):
        """Get the barcode format.
        
        Returns:
            str: The barcode format (PKBarcodeFormat* constant).
        """
        return self._format
    
    @format.setter
    def format(self, value):
        """Set the barcode format.
        
        Args:
            value (str): The barcode format (must be a valid BarcodeFormat constant).
        
        Raises:
            ValueError: If format is not a valid BarcodeFormat constant.
        """
        valid_formats = [
            BarcodeFormat.PDF417,
            BarcodeFormat.QR,
            BarcodeFormat.AZTEC,
            BarcodeFormat.CODE128,
        ]
        if value not in valid_formats:
            raise ValueError(
                f"Invalid barcode format: {value}. Must be one of: "
                f"BarcodeFormat.PDF417, BarcodeFormat.QR, BarcodeFormat.AZTEC, "
                f"or BarcodeFormat.CODE128"
            )
        self._format = value
    
    @property
    def message_encoding(self):
        """Get the message encoding.
        
        Returns:
            str: The character encoding name.
        """
        return self.messageEncoding
    
    @property
    def alt_text(self):
        """Get the alternative text displayed near the barcode.
        
        Returns:
            str or None: The alternative text, or None if not set.
        """
        return getattr(self, 'altText', None)
    
    def json_dict(self):
        """Generate JSON-serializable dictionary representation of the barcode.
        
        Creates a dictionary containing all barcode properties, excluding None
        values. The dictionary follows the Apple Wallet pass.json specification
        format for barcode objects.
        
        Returns:
            dict: A dictionary with keys:
                - format (str): The barcode format constant
                - message (str): The barcode message/payload
                - messageEncoding (str): The character encoding
                - altText (str, optional): Alternative text if set
        
        Examples:
            >>> barcode = Barcode("12345", BarcodeFormat.QR, alt_text="ID: 12345")
            >>> barcode.json_dict()
            {
                'format': 'PKBarcodeFormatQR',
                'message': '12345',
                'messageEncoding': 'iso-8859-1',
                'altText': 'ID: 12345'
            }
            
            >>> barcode = Barcode("ABCDEF")
            >>> barcode.json_dict()
            {
                'format': 'PKBarcodeFormatPDF417',
                'message': 'ABCDEF',
                'messageEncoding': 'iso-8859-1'
            }
        """
        result = {
            "format": self.format,
            "message": self.message,
            "messageEncoding": self.messageEncoding,
        }
        
        # Only include altText if it was explicitly set
        if hasattr(self, 'altText') and self.altText is not None:
            result["altText"] = self.altText
        
        return result
    
    def __repr__(self):
        """Return a string representation of the Barcode instance.
        
        Returns:
            str: A string representation including format and message preview.
        """
        message_preview = self.message[:20] + "..." if len(self.message) > 20 else self.message
        alt_text_info = f", alt_text='{self.altText}'" if hasattr(self, 'altText') else ""
        return f"Barcode(format={self.format}, message='{message_preview}'{alt_text_info})"
    
    def __eq__(self, other):
        """Compare two Barcode instances for equality.
        
        Args:
            other: Another object to compare with.
        
        Returns:
            bool: True if both barcodes have the same format, message, encoding,
                and alternative text.
        """
        if not isinstance(other, Barcode):
            return False
        return (
            self.format == other.format
            and self.message == other.message
            and self.messageEncoding == other.messageEncoding
            and self.alt_text == other.alt_text
        )
