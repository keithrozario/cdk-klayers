from aws_cdk import aws_lambda
import cdk_klayers.exceptions as exceptions
import requests
import json


class Klayers:

    base_url = "https://api.klayers.cloud/api/v2"

    def __init__(self, scope, python_version: aws_lambda.Runtime, region=False):
        """
        Args:
            scope: The Construct in which you want to use Klayers, typically this is the STACK
            python_version: The python version for layers you want
            region: The AWS region to deploy into, if no region is supplied the region from the CDK environment is used
        """

        self.python_version = self.get_python_version(python_version)
        self.region = self.get_region(scope, region)

        # Get Latest Layers for the region & python_version
        self.latest_layer_arns = self.get_latest_layer_arns(
            region=self.region, python_version=python_version
        )

        return None

    def layer_version(self, scope, package, layer_version="latest"):
        """
        Args:
            scope: The Construct in which you want to use Klayers, typically this is the Stack
            package: The Python package you wish to use
            layer_version: The version of the LambdaLayer you wish to use, set to 'latest' for the latest
        """

        try:
            latest_layer_version_arn = self.latest_layer_arns[package]["arn"]
        except KeyError:
            raise exceptions.LayerNameDoesNotExists(
                message=f"No Package named '{package}' could be found. \
                    Package name must be one of the following: {self.latest_layer_arns.keys()}"
            )

        if layer_version == "latest":
            layer_version_arn = latest_layer_version_arn
        else:
            arn_components = latest_layer_version_arn.split(":")
            try:
                arn_components[7] = str(int(layer_version))
            except (ValueError, TypeError):
                raise exceptions.LayerVersionError(
                    message=f"layer_version must be a string that is convertible to integer. Instead {layer_version} received"
                )
            layer_version_arn = ":".join(arn_components)

        lambda_layer_version = aws_lambda.LayerVersion.from_layer_version_arn(
            scope,
            id=f"{self.region}-{self.python_version}-{package}-{layer_version}",
            layer_version_arn=layer_version_arn,
        )

        return lambda_layer_version

    def get_region(self, scope, region=False) -> str:
        """
        Retrieves the region from the environment.
        """
        if not region:
            region = scope.environment.split("/")[3]
            if region == "unknown-region":
                raise exceptions.NoRegionProvidedError(
                    "No region was provided. Please include region as a CDK environment or in the Klayers Class initialization"
                )
        else:
            region = region

        return region

    def get_latest_layer_arns(self, region: str, python_version: str) -> dict:
        """
        Gets latest layers for region and python_version
        returns:
            latest_layers: List of dict each with package as key and attrs of packageVersion, arn, package
        """

        url_python_version = python_version.to_string().replace("python", "p")
        latest_layers = requests.get(
            f"{self.base_url}/{url_python_version}/layers/latest/{region}/"
        )

        # Api returns a list, convert to dict
        layers = json.loads(latest_layers.content)
        layers_dict = dict()
        for layer in layers:
            _key = layer["package"]
            _value = {"arn": layer["arn"], "packageVersion": layer["packageVersion"]}
            layers_dict[_key] = _value

        return layers_dict

    def get_python_version(self, python_version: aws_lambda.Runtime) -> str:
        """
        Return a python version of the runtime, in form of (e.g. python3.12)
        """

        if isinstance(python_version, aws_lambda.Runtime):
            python_version_str = python_version.to_string()
        else:
            raise exceptions.InvalidPythonVersion(
                message=f"python_version must be of type aws_lambda.Runtime, e.g. aws_lambda.Runtime.PYTHON_3_12. Got {python_version} instead"
            )

        return python_version_str
