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

class LayerVersionNotInteger(KlayersError):
    """
    Layer Version Provided cannot be converted to integer
    """
    def __init__(self, message):
        self.message = message
        self.Code = "LayerVersionNotInteger"

class LayerNameDoesNotExists(KlayersError):
    """
    Layer Name does not exists
    """

    def __init__(self, message):
        self.message = message
        self.Code = "LayerNameDoesNotExists"

class InvalidPythonVersion(KlayersError):
    """
    Python Version not provided as a aws_lambda.Runtime type
    """

    def __init__(self, message):
        self.message = message
        self.Code = "InvalidPythonVersion"
