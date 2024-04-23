def validate_layer_arn(arn: str) -> bool:
    """
    Validates if an arn is valid, and returns True or False
    """
    valid_arn = True

    try:
        arn_components = arn.split(":")
        assert len(arn_components) == 8
        assert arn_components[0] == "arn"
        assert arn_components[1] == "aws"
        assert arn_components[2] == "lambda"
        assert arn_components[5] == "layer"

        # Account ID is as 12 digit code
        assert len(str(int(arn_components[4]))) == 12
        # Layer Version is an int
        assert isinstance(int(arn_components[7]), int)

    except (AssertionError, AttributeError):
        valid_arn = False

    return valid_arn
