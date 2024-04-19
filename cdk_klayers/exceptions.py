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