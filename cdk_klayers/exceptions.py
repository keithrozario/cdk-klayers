class KlayersError(Exception):
    """
    Base class for exceptions in this module.
    """

    pass


class NoRegionProvidedError(KlayersError):
    """
    No region provided, unable to find klayers layer
    """

    def __init__(self, message):
        self.message = message
        self.Code = "NoRegionProvidedError"
        super().__init__(self.message)


class LayerVersionNotInteger(KlayersError):
    """
    Layer Version Provided cannot be converted to integer
    """

    def __init__(self, message):
        self.message = message
        self.Code = "LayerVersionNotInteger"
        super().__init__(self.message)


class LayerNameDoesNotExists(KlayersError):
    """
    Layer Name does not exists
    """

    def __init__(self, message):
        self.message = message
        self.Code = "LayerNameDoesNotExists"
        super().__init__(self.message)


class InvalidPythonVersion(KlayersError):
    """
    Python Version not provided as a aws_lambda.Runtime type
    """

    def __init__(self, message):
        self.message = message
        self.Code = "InvalidPythonVersion"
        super().__init__(self.message)

class RequestException(KlayersError):
    """
    Unable to connect to the API
    """

    def __init__(self, message):
        self.message = message
        self.Code = "RequestException"
        super().__init__(self.message)
