from aws_cdk import aws_lambda

class Klayers():
    def __init__(self, python_version, region):
        self.python_version = python_version.to_string()
        self.region = region

    def layer_version(self, scope, package, layer_version="latest"):
        lambda_layer_version = aws_lambda.LayerVersion.from_layer_version_arn(
            scope,
            id=f"{self.region}-{self.python_version}-{package}-{layer_version}",
            layer_version_arn=f"arn:aws:lambda:{self.region}:770693421928:layer:Klayers-p312-{package}:3"
        )

        return lambda_layer_version

def get_layers(scope, region: str, package: str, python_version: str, layer_version: str="latest"):

        lambda_layer_version = aws_lambda.LayerVersion.from_layer_version_arn(
        scope,
        id=f"{region}-{python_version}-{package}-{layer_version}-method",
        layer_version_arn=f"arn:aws:lambda:{region}:770693421928:layer:Klayers-p312-{package}:3"
        )

        return lambda_layer_version