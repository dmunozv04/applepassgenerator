"""Apple Pass base class with full iOS 6.0-18.0 support

This module contains the refactored ApplePass class that supports:
- Multiple barcodes (iOS 9.0+)
- Multiple locations and beacons (max 10 each)
- Multiple relevant dates (iOS 18.0+)
- Semantic tags (iOS 12.0+)
- Personalization (iOS 10.0+)
- NFC (iOS 9.0+)
- Grouping and sharing control
- Legacy backward compatibility
"""

# Standard Library
import decimal
import hashlib
import json
import zipfile
import warnings
from io import BytesIO

# Third Party Stuff
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs7

# Local imports - use refactored classes from separate modules
from .barcodes import Barcode
from .constants import BarcodeFormat
from .locations import Location, IBeacon
from .relevant_date import RelevantDate


class ApplePass(object):
    """Apple Wallet Pass generator
    
    Generates .pkpass files compatible with Apple Wallet.
    Supports iOS 6.0+ features up to iOS 18.0.
    
    This refactored class supports:
    - Multiple barcodes via add_barcode() (iOS 9.0+)
    - Multiple locations via add_location() (max 10)
    - Multiple beacons via add_beacon() (max 10)
    - Multiple relevant dates via add_relevant_date() (iOS 18.0+)
    - Semantic tags for rich data (iOS 12.0+)
    - Personalization (iOS 10.0+)
    - NFC support (iOS 9.0+)
    - Grouping and sharing control
    
    Legacy backward compatibility is maintained by generating both
    modern array fields and legacy singular fields.
    
    Args:
        pass_information: PassInformation subclass (BoardingPass, Coupon, etc.)
        pass_type_identifier (str): Pass type ID from Apple
        organization_name (str): Organization display name
        team_identifier (str): Team ID from Apple Developer account
    
    Example:
        >>> from applepassgenerator.models import Coupon, ApplePass, Barcode, Location
        >>> 
        >>> # Create pass information
        >>> coupon = Coupon()
        >>> coupon.add_primary_field('offer', '20% Off', 'Special Offer')
        >>> 
        >>> # Create pass
        >>> apple_pass = ApplePass(
        ...     coupon,
        ...     pass_type_identifier='pass.com.example.coupon',
        ...     organization_name='Example Corp',
        ...     team_identifier='A1B2C3D4E5'
        ... )
        >>> 
        >>> # Set required fields
        >>> apple_pass.serial_number = 'COUP-12345'
        >>> apple_pass.description = '20% off coupon'
        >>> 
        >>> # Add modern features
        >>> apple_pass.add_barcode(Barcode('12345', BarcodeFormat.QR))
        >>> apple_pass.add_location(Location(37.33, -122.03))
        >>> apple_pass.add_relevant_date('2026-03-15T19:00:00-08:00')
        >>> 
        >>> # Generate .pkpass file
        >>> pass_file = apple_pass.create('cert.pem', 'key.pem', 'wwdr.pem', 'password')
    """
    
    def __init__(
        self,
        pass_information,
        pass_type_identifier="",
        organization_name="",
        team_identifier="",
    ):
        self._files = {}  # Files to include in .pkpass
        self._hashes = {}  # SHA-1 hashes of files for manifest
        
        # ===== REQUIRED FIELDS (iOS 6.0+) =====
        self.pass_type_identifier = pass_type_identifier  # passTypeIdentifier
        self.organization_name = organization_name  # organizationName
        self.team_identifier = team_identifier  # teamIdentifier
        self.serial_number = ""  # serialNumber - MUST be set before create()
        self.description = ""  # description - MUST be set before create()
        self.format_version = 1  # formatVersion - Always 1
        
        # ===== VISUAL APPEARANCE (iOS 6.0+, Optional) =====
        self.background_color = None  # backgroundColor - rgb(r, g, b)
        self.foreground_color = None  # foregroundColor
        self.label_color = None  # labelColor
        self.logo_text = None  # logoText
        self.suppress_strip_shine = False  # suppressStripShine
        
        # ===== BARCODES (Refactored) =====
        # API CHANGE: Use add_barcode() instead of self.barcode = 
        # Generates both 'barcodes' array (iOS 9.0+) and legacy 'barcode' field
        self._barcodes = []  # Internal list of Barcode objects
        
        # ===== WEB SERVICE (iOS 6.0+, Optional) =====
        self.web_service_url = None  # webServiceURL
        self.authentication_token = None  # authenticationToken (min 16 chars)
        
        # ===== RELEVANCE - LOCATIONS & BEACONS (Refactored) =====
        # API CHANGE: Use add_location() and add_beacon()
        self._locations = []  # Internal list (max 10)
        self._beacons = []  # Internal list (max 10)
        
        # ===== RELEVANCE - DATES (Refactored) =====
        # API CHANGE: Use add_relevant_date()
        # Generates both 'relevantDates' (iOS 18.0+) and legacy 'relevantDate'
        self._relevant_dates = []  # Internal list of RelevantDate objects or ISO 8601 strings
        
        # ===== NEW FEATURES =====
        self.nfc = None  # NFC object (iOS 9.0+)
        self.semantics = None  # SemanticTags object (iOS 12.0+)
        self.personalization = None  # Personalization object (iOS 10.0+)
        self.grouping_identifier = None  # groupingIdentifier (iOS 7.0+)
        self.sharing_prohibited = None  # sharingProhibited (iOS 11.0+)
        self.upcoming_event_info = None  # List of UpcomingPassInformationEntry (iOS 18.0+)
        
        # ===== ASSOCIATED APPS (iOS 6.0+, Optional) =====
        self.associated_store_identifiers = None  # associatedStoreIdentifiers
        self.app_launch_url = None  # appLaunchURL
        
        # ===== PASS BEHAVIOR (Optional) =====
        self.expiration_date = None  # expirationDate (iOS 7.0+)
        self.voided = None  # voided (iOS 7.0+)
        self.user_info = None  # userInfo - Custom JSON data
        
        # Pass content
        self.pass_information = pass_information

    def __setattr__(self, name, value):
        """Handle attribute setting with deprecation warnings
        
        Provides backward compatibility for legacy single-value APIs
        by redirecting to new add_* methods with deprecation warnings.
        """
        # Handle deprecation warnings for legacy API
        if name == 'barcode' and not name.startswith('_'):
            warnings.warn(
                "Setting 'barcode' directly is deprecated. Use add_barcode() instead. "
                "This will be removed in version 0.2.0.",
                DeprecationWarning,
                stacklevel=2
            )
            if value is not None:
                self.add_barcode(value)
            return
        
        if name == 'locations' and not name.startswith('_'):
            warnings.warn(
                "Setting 'locations' directly is deprecated. Use add_location() instead. "
                "This will be removed in version 0.2.0.",
                DeprecationWarning,
                stacklevel=2
            )
            if value is not None:
                if isinstance(value, list):
                    for loc in value:
                        self.add_location(loc)
                else:
                    self.add_location(value)
            return
        
        if name == 'ibeacons' and not name.startswith('_'):
            warnings.warn(
                "Setting 'ibeacons' directly is deprecated. Use add_beacon() instead. "
                "This will be removed in version 0.2.0.",
                DeprecationWarning,
                stacklevel=2
            )
            if value is not None:
                if isinstance(value, list):
                    for beacon in value:
                        self.add_beacon(beacon)
                else:
                    self.add_beacon(value)
            return
        
        if name == 'relevant_date' and not name.startswith('_'):
            warnings.warn(
                "Setting 'relevant_date' directly is deprecated. Use add_relevant_date() instead. "
                "This will be removed in version 0.2.0.",
                DeprecationWarning,
                stacklevel=2
            )
            if value is not None:
                self.add_relevant_date(value)
            return
        
        # Normal attribute setting
        super().__setattr__(name, value)

    # ===== NEW METHODS FOR MODERN API =====
    
    def add_barcode(self, barcode):
        """Add a barcode to the pass (iOS 9.0+ API)
        
        Supports multiple barcodes. The pass.json will include both:
        - 'barcodes' array (iOS 9.0+)
        - 'barcode' singular field (iOS 6.0-8.0) for backward compatibility
        
        Args:
            barcode (Barcode): Barcode object to add
        
        Raises:
            TypeError: If barcode is not a Barcode instance
        
        Example:
            >>> from applepassgenerator.models import Barcode, BarcodeFormat
            >>> apple_pass.add_barcode(Barcode('12345678', BarcodeFormat.QR))
            >>> apple_pass.add_barcode(Barcode('87654321', BarcodeFormat.CODE128))
        """
        if not isinstance(barcode, Barcode):
            raise TypeError(f"barcode must be a Barcode instance, got {type(barcode).__name__}")
        self._barcodes.append(barcode)
    
    def add_location(self, location):
        """Add a location for pass relevance (max 10)
        
        Locations trigger pass display when user is nearby.
        Apple Wallet allows up to 10 locations per pass.
        
        Args:
            location (Location): Location object to add
        
        Raises:
            TypeError: If location is not a Location instance
            ValueError: If maximum 10 locations exceeded
        
        Example:
            >>> from applepassgenerator.models import Location
            >>> # Store location
            >>> apple_pass.add_location(Location(37.33182, -122.03118))
            >>> # Additional location
            >>> apple_pass.add_location(Location(40.7128, -74.0060))
        """
        if not isinstance(location, Location):
            raise TypeError(f"location must be a Location instance, got {type(location).__name__}")
        if len(self._locations) >= 10:
            raise ValueError("Maximum 10 locations allowed per pass")
        self._locations.append(location)
    
    def add_beacon(self, beacon):
        """Add an iBeacon for pass relevance (max 10)
        
        Beacons trigger pass display when user is near the beacon.
        Apple Wallet allows up to 10 beacons per pass.
        
        Args:
            beacon (IBeacon): IBeacon object to add
        
        Raises:
            TypeError: If beacon is not an IBeacon instance
            ValueError: If maximum 10 beacons exceeded
        
        Example:
            >>> from applepassgenerator.models import IBeacon
            >>> apple_pass.add_beacon(IBeacon('E2C56DB5-DFFB-48D2-B060-D0F5A71096E0', 123, 456))
        """
        if not isinstance(beacon, IBeacon):
            raise TypeError(f"beacon must be an IBeacon instance, got {type(beacon).__name__}")
        if len(self._beacons) >= 10:
            raise ValueError("Maximum 10 beacons allowed per pass")
        self._beacons.append(beacon)
    
    def add_relevant_date(self, date):
        """Add a relevant date for pass display (iOS 18.0+ API)
        
        Relevant dates trigger pass display at specific times.
        Multiple dates supported in iOS 18.0+.
        
        The pass.json will include both:
        - 'relevantDates' array (iOS 18.0+) with RelevantDate objects
        - 'relevantDate' singular field (iOS 6.0-17.0) for backward compatibility
        
        Args:
            date (RelevantDate or str): RelevantDate object or ISO 8601 date string.
                String format is supported for backward compatibility and will be
                converted to a RelevantDate object.
        
        Raises:
            TypeError: If date is not a RelevantDate or string
        
        Examples:
            >>> # Using RelevantDate object (recommended)
            >>> from applepassgenerator import RelevantDate
            >>> apple_pass.add_relevant_date(RelevantDate(date='2026-03-15T19:00:00-08:00'))
            
            >>> # Using string for backward compatibility
            >>> apple_pass.add_relevant_date('2026-03-15T19:00:00-08:00')
            
            >>> # Using date interval
            >>> apple_pass.add_relevant_date(RelevantDate(
            ...     start_date='2026-03-15T18:00:00-08:00',
            ...     end_date='2026-03-15T22:00:00-08:00'
            ... ))
        
        Note:
            Date format must be ISO 8601: YYYY-MM-DDTHH:MM:SS±HH:MM
        """
        if isinstance(date, str):
            # Backward compatibility: convert string to RelevantDate
            date = RelevantDate(date=date)
        elif not isinstance(date, RelevantDate):
            raise TypeError(
                f"date must be a RelevantDate instance or string, got {type(date).__name__}"
            )
        self._relevant_dates.append(date)

    # ===== EXISTING METHODS (Preserved) =====
    
    def add_file(self, name, fd):
        """Add a file to the pass package
        
        Required files: icon.png, logo.png (and @2x, @3x versions)
        Optional: strip.png, background.png, thumbnail.png, footer.png
        
        Args:
            name (str): Filename (e.g., 'icon.png', 'logo@2x.png')
            fd: File-like object with read() method
        
        Example:
            >>> with open('icon.png', 'rb') as f:
            ...     apple_pass.add_file('icon.png', f)
            >>> with open('logo@2x.png', 'rb') as f:
            ...     apple_pass.add_file('logo@2x.png', f)
        """
        self._files[name] = fd.read()
    
    def create(self, certificate, key, wwdr_certificate, password, zip_file=None):
        """Generate the .pkpass file
        
        Creates a signed .pkpass file containing:
        - pass.json (pass data)
        - manifest.json (file hashes)
        - signature (PKCS#7 signature)
        - All added files (icons, images, etc.)
        
        Args:
            certificate (str): Path to certificate.pem file
            key (str): Path to private key file
            wwdr_certificate (str): Path to Apple WWDR certificate
            password (str): Certificate password
            zip_file (str/BytesIO, optional): Output path or BytesIO object
        
        Returns:
            BytesIO: The generated .pkpass file
        
        Raises:
            ValueError: If required fields (serial_number, description) not set
        
        Example:
            >>> pass_file = apple_pass.create(
            ...     'certificate.pem',
            ...     'key.pem',
            ...     'wwdr.pem',
            ...     'my_password'
            ... )
            >>> # Save to file
            >>> with open('mypass.pkpass', 'wb') as f:
            ...     f.write(pass_file.getvalue())
        """
        # Validation
        if not self.serial_number:
            raise ValueError("serial_number is required")
        if not self.description:
            raise ValueError("description is required")
        
        pass_json = self._create_pass_json()
        manifest = self._create_manifest(pass_json)
        signature = self._create_signature_crypto(
            manifest, certificate, key, wwdr_certificate, password
        )
        
        if not zip_file:
            zip_file = BytesIO()
        self._create_zip(pass_json, manifest, signature, zip_file=zip_file)
        return zip_file

    def _create_pass_json(self):
        """Generate pass.json content
        
        Returns:
            str: JSON string of pass data
        """
        return json.dumps(self, default=pass_handler)

    def _create_manifest(self, pass_json):
        """Create manifest.json with SHA-1 hashes of all files
        
        Args:
            pass_json (str): The pass.json content
        
        Returns:
            str: JSON string of file hashes
        """
        self._hashes["pass.json"] = hashlib.sha1(pass_json.encode("utf-8")).hexdigest()
        for filename, filedata in self._files.items():
            self._hashes[filename] = hashlib.sha1(filedata).hexdigest()
        return json.dumps(self._hashes)

    def _read_file_bytes(self, path):
        """Read file as bytes
        
        Args:
            path (str): File path
        
        Returns:
            bytes: File contents
        """
        with open(path, 'rb') as file:
            return file.read()

    def _create_signature_crypto(self, manifest, certificate, key, wwdr_certificate, password):
        """Create PKCS#7 signature of manifest
        
        Args:
            manifest (str): Manifest JSON string
            certificate (str): Path to certificate file
            key (str): Path to private key file
            wwdr_certificate (str): Path to WWDR certificate
            password (str): Certificate password
        
        Returns:
            bytes: DER-encoded PKCS#7 signature
        """
        cert = x509.load_pem_x509_certificate(self._read_file_bytes(certificate))
        priv_key = serialization.load_pem_private_key(
            self._read_file_bytes(key), 
            password=password.encode("UTF-8")
        )
        wwdr_cert = x509.load_pem_x509_certificate(
            self._read_file_bytes(wwdr_certificate)
        )
        
        options = [pkcs7.PKCS7Options.DetachedSignature]
        return (
            pkcs7.PKCS7SignatureBuilder()
            .set_data(manifest.encode("UTF-8"))
            .add_signer(cert, priv_key, hashes.SHA1())
            .add_certificate(wwdr_cert)
            .sign(serialization.Encoding.DER, options)
        )

    def _create_zip(self, pass_json, manifest, signature, zip_file=None):
        """Create .pkpass ZIP archive
        
        Args:
            pass_json (str): Pass JSON content
            manifest (str): Manifest JSON content
            signature (bytes): PKCS#7 signature
            zip_file (str/BytesIO, optional): Output destination
        """
        zf = zipfile.ZipFile(zip_file or "pass.pkpass", "w")
        zf.writestr("signature", signature)
        zf.writestr("manifest.json", manifest)
        zf.writestr("pass.json", pass_json)
        for filename, filedata in self._files.items():
            zf.writestr(filename, filedata)
        zf.close()

    def json_dict(self):
        """Generate pass.json dictionary
        
        This method handles:
        - Legacy field generation (barcode, relevantDate) for iOS 6.0-9.0
        - Modern field population (barcodes, relevantDates) for iOS 9.0+/18.0+
        - Conditional inclusion of optional fields
        - Proper camelCase naming for Apple Wallet compatibility
        
        Returns:
            dict: Dictionary representation for pass.json
        """
        # Required fields
        d = {
            "description": self.description,
            "formatVersion": self.format_version,
            "organizationName": self.organization_name,
            "passTypeIdentifier": self.pass_type_identifier,
            "serialNumber": self.serial_number,
            "teamIdentifier": self.team_identifier,
            "suppressStripShine": self.suppress_strip_shine,
            self.pass_information.jsonname: self.pass_information.json_dict(),
        }
        
        # ===== BARCODES: Generate both modern and legacy =====
        if self._barcodes:
            # Modern: 'barcodes' array (iOS 9.0+)
            d["barcodes"] = [b.json_dict() for b in self._barcodes]
            
            # Legacy: 'barcode' singular (iOS 6.0-8.0) for backward compatibility
            # Use first barcode, ensure it's a legacy format
            first_barcode = self._barcodes[0]
            legacy_formats = [BarcodeFormat.PDF417, BarcodeFormat.QR, BarcodeFormat.AZTEC]
            
            if first_barcode.format in legacy_formats:
                d["barcode"] = first_barcode.json_dict()
            else:
                # Convert CODE128 to PDF417 for legacy devices
                legacy_barcode = Barcode(
                    first_barcode.message,
                    BarcodeFormat.PDF417,
                    getattr(first_barcode, 'altText', ''),
                    first_barcode.messageEncoding
                )
                d["barcode"] = legacy_barcode.json_dict()
        
        # ===== RELEVANCE: DATES =====
        if self._relevant_dates:
            # Modern: 'relevantDates' array (iOS 18.0+)
            # Apple expects array elements to have "date" key or "startDate"/"endDate" pair
            relevant_dates_array = []
            for date_obj in self._relevant_dates:
                date_entry = {}
                if date_obj.date:
                    # Simple date object
                    date_entry["date"] = date_obj.date
                if date_obj.startDate:
                    # Date interval start
                    date_entry["startDate"] = date_obj.startDate
                if date_obj.endDate:
                    # Date interval end
                    date_entry["endDate"] = date_obj.endDate
                
                # Only add if we have at least one date field
                if date_entry:
                    relevant_dates_array.append(date_entry)
            
            # Only include relevantDates if we have valid entries
            if relevant_dates_array:
                d["relevantDates"] = relevant_dates_array
            
            # Legacy: 'relevantDate' singular (iOS 6.0-17.0) for backward compatibility
            # Use the 'date' field from the first RelevantDate, or startDate if no date specified
            first_date = self._relevant_dates[0]
            if first_date.date:
                d["relevantDate"] = first_date.date
            elif first_date.startDate:
                d["relevantDate"] = first_date.startDate
            else:
                # Should never happen due to RelevantDate validation, but just in case
                d["relevantDate"] = first_date.endDate
        
        # ===== RELEVANCE: LOCATIONS =====
        if self._locations:
            d["locations"] = [loc.json_dict() for loc in self._locations]
        
        # ===== RELEVANCE: BEACONS =====
        if self._beacons:
            d["beacons"] = [beacon.json_dict() for beacon in self._beacons]
        
        # ===== VISUAL APPEARANCE =====
        if self.background_color:
            d["backgroundColor"] = self.background_color
        if self.foreground_color:
            d["foregroundColor"] = self.foreground_color
        if self.label_color:
            d["labelColor"] = self.label_color
        if self.logo_text:
            d["logoText"] = self.logo_text
        
        # ===== WEB SERVICE =====
        if self.web_service_url:
            d["webServiceURL"] = self.web_service_url
            d["authenticationToken"] = self.authentication_token
        
        # ===== ASSOCIATED APPS =====
        if self.associated_store_identifiers:
            d["associatedStoreIdentifiers"] = self.associated_store_identifiers
        if self.app_launch_url:
            d["appLaunchURL"] = self.app_launch_url
        
        # ===== PASS BEHAVIOR =====
        if self.expiration_date:
            d["expirationDate"] = self.expiration_date
        if self.voided:
            d["voided"] = True
        if self.user_info:
            d["userInfo"] = self.user_info
        
        # ===== GROUPING & SHARING (iOS 7.0+) =====
        if self.grouping_identifier:
            d["groupingIdentifier"] = self.grouping_identifier
        if self.sharing_prohibited is not None:
            d["sharingProhibited"] = self.sharing_prohibited
        
        # ===== NFC (iOS 9.0+) =====
        if self.nfc:
            d["nfc"] = self.nfc.json_dict()
        
        # ===== SEMANTIC TAGS (iOS 12.0+) =====
        if self.semantics:
            d["semantics"] = self.semantics.json_dict()
        
        # ===== PERSONALIZATION (iOS 10.0+) =====
        if self.personalization:
            d["personalization"] = self.personalization.json_dict()
        
        # ===== UPCOMING EVENTS (iOS 18.0+) =====
        if self.upcoming_event_info:
            d["upcomingEventInfo"] = [
                event.json_dict() for event in self.upcoming_event_info
            ]
        
        return d


def pass_handler(obj):
    """JSON serialization handler for custom objects
    
    Enables JSON serialization of ApplePass and related objects
    by calling their json_dict() method.
    
    Args:
        obj: Object to serialize
    
    Returns:
        Serializable representation of the object
    """
    if hasattr(obj, "json_dict"):
        return obj.json_dict()
    elif isinstance(obj, decimal.Decimal):
        return str(obj)
    else:
        return obj
