"""
Personalization models for Apple Wallet passes.

This module provides classes and constants for implementing pass personalization,
allowing users to provide personal information before adding a pass to their wallet.

iOS 10.0+
"""


class PersonalizationField:
    """Personalization field name constants.
    
    iOS 10.0+
    
    These constants specify which personal information fields can be requested
    from users when they add a pass to their wallet.
    """
    NAME = "PKPassPersonalizationFieldName"
    POSTAL_CODE = "PKPassPersonalizationFieldPostalCode"
    EMAIL_ADDRESS = "PKPassPersonalizationFieldEmailAddress"
    PHONE_NUMBER = "PKPassPersonalizationFieldPhoneNumber"


class Personalization:
    """Personalization configuration for passes.
    
    iOS 10.0+
    
    Personalization allows users to provide personal information before adding
    a pass to their wallet. This is useful for passes that need to be customized
    with user-specific data, such as membership cards, loyalty cards, or tickets.
    
    When personalization is configured, the user sees a form requesting the
    specified information before the pass is added to their wallet. Your server
    can then generate a personalized pass based on this information.
    
    Attributes:
        requiredPersonalizationFields (list): List of required field names.
            Use PersonalizationField constants for field names.
        description (str): Description text shown to the user explaining why
            the information is needed.
        termsAndConditions (str): Terms and conditions text that the user must
            accept before providing information.
    
    Example:
        >>> # Create a simple personalization request
        >>> personalization = Personalization(
        ...     required_fields=[
        ...         PersonalizationField.NAME,
        ...         PersonalizationField.EMAIL_ADDRESS
        ...     ],
        ...     description="Please provide your name and email to personalize your pass."
        ... )
        >>> 
        >>> # Create with terms and conditions
        >>> personalization = Personalization(
        ...     required_fields=[
        ...         PersonalizationField.NAME,
        ...         PersonalizationField.EMAIL_ADDRESS,
        ...         PersonalizationField.PHONE_NUMBER
        ...     ],
        ...     description="To personalize your loyalty card, please provide your information.",
        ...     terms_and_conditions="By providing this information, you agree to receive "
        ...                          "promotional emails and SMS messages from our store."
        ... )
        >>> 
        >>> # Add to a pass
        >>> from applepassgenerator.client import ApplePassClient
        >>> pass_data = {...}
        >>> pass_data['personalization'] = personalization.json_dict()
        
        >>> # Full example with a store card
        >>> personalization = Personalization(
        ...     required_fields=[
        ...         PersonalizationField.NAME,
        ...         PersonalizationField.EMAIL_ADDRESS,
        ...         PersonalizationField.POSTAL_CODE
        ...     ],
        ...     description="Join our rewards program! Provide your information "
        ...                 "to create your personalized membership card.",
        ...     terms_and_conditions="By joining our rewards program, you agree to our "
        ...                          "privacy policy and terms of service. We will use your "
        ...                          "information to track purchases and send you exclusive offers."
        ... )
    
    Note:
        - The fields you request should match the information your pass web service
          expects to receive when generating personalized passes.
        - All specified fields are required - users cannot skip any fields.
        - Keep the description and terms short and clear for the best user experience.
        - The user's device will send the collected information to your web service
          at the URL specified by the authenticationToken and webServiceURL keys.
    
    Reference:
        https://developer.apple.com/documentation/walletpasses/pass/personalization
    """
    
    def __init__(self, required_fields, description="", terms_and_conditions=""):
        """Initialize a Personalization configuration.
        
        Args:
            required_fields (list): List of field names required from the user.
                Valid values are PersonalizationField constants:
                - PersonalizationField.NAME ("PKPassPersonalizationFieldName")
                - PersonalizationField.POSTAL_CODE ("PKPassPersonalizationFieldPostalCode")
                - PersonalizationField.EMAIL_ADDRESS ("PKPassPersonalizationFieldEmailAddress")
                - PersonalizationField.PHONE_NUMBER ("PKPassPersonalizationFieldPhoneNumber")
            description (str, optional): Description text shown to the user explaining
                why their information is needed. Defaults to "".
            terms_and_conditions (str, optional): Terms and conditions text that the
                user must accept. If provided, adds a terms acceptance requirement.
                Defaults to "".
        
        Raises:
            ValueError: If required_fields is empty or contains invalid field names.
            TypeError: If required_fields is not a list.
        
        Example:
            >>> personalization = Personalization(
            ...     required_fields=[
            ...         PersonalizationField.NAME,
            ...         PersonalizationField.EMAIL_ADDRESS
            ...     ],
            ...     description="Please provide your information to personalize your pass."
            ... )
        """
        if not isinstance(required_fields, list):
            raise TypeError("required_fields must be a list")
        
        if not required_fields:
            raise ValueError("required_fields cannot be empty")
        
        # Validate field names
        valid_fields = {
            PersonalizationField.NAME,
            PersonalizationField.POSTAL_CODE,
            PersonalizationField.EMAIL_ADDRESS,
            PersonalizationField.PHONE_NUMBER,
        }
        
        for field in required_fields:
            if field not in valid_fields:
                raise ValueError(
                    f"Invalid personalization field: {field}. "
                    f"Valid fields are: {', '.join(sorted(valid_fields))}"
                )
        
        self.requiredPersonalizationFields = required_fields
        self.description = description
        if terms_and_conditions:
            self.termsAndConditions = terms_and_conditions
    
    def json_dict(self):
        """Convert the Personalization object to a JSON-serializable dictionary.
        
        Returns:
            dict: A dictionary representation suitable for inclusion in pass.json.
                The dictionary contains:
                - requiredPersonalizationFields (list): Required field names
                - description (str, optional): Description text if provided
                - termsAndConditions (str, optional): Terms text if provided
        
        Example:
            >>> personalization = Personalization(
            ...     required_fields=[PersonalizationField.NAME],
            ...     description="Provide your name"
            ... )
            >>> personalization.json_dict()
            {
                'requiredPersonalizationFields': ['PKPassPersonalizationFieldName'],
                'description': 'Provide your name'
            }
        """
        d = {"requiredPersonalizationFields": self.requiredPersonalizationFields}
        
        if self.description:
            d["description"] = self.description
        
        if hasattr(self, 'termsAndConditions'):
            d["termsAndConditions"] = self.termsAndConditions
        
        return d
    
    def __repr__(self):
        """Return a string representation of the Personalization object.
        
        Returns:
            str: A string representation showing the required fields.
        """
        fields_str = ", ".join(self.requiredPersonalizationFields)
        return f"Personalization(required_fields=[{fields_str}])"
