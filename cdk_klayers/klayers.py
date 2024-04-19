from aws_cdk import aws_lambda
import cdk_klayers.exceptions as exceptions

class Klayers():

    base_url = "https://api.klayers.cloud/api/v2/"

    def __init__(self, scope, python_version: aws_lambda.Runtime, packages: list=[], region=False):
        """
        Args:
            scope: The Construct in which you want to use Klayers, typically this is the STACK
            python_version: The python version for layers you want
            region: The AWS region to deploy into, if no region is supplied the region from the CDK environment is used
        """

        self.python_version = python_version.to_string()
        self.region = self.get_region(scope)

        # TO DO - construct package list for the region
        latest_layer_arns = self.get_latest_layer_arns(region=self.region, python_version=python_version)

        # TO DO - construct layers list
        pass
            
    def layer_version(self, scope, package, layer_version="latest"):
        """
        Args:
            scope: The Construct in which you want to use Klayers, typically this is the Stack
            package: The Python package you wish to use
            layer_version: The version of the LambdaLayer you wish to use, set to 'latest' for the latest
        """

        # TO DO - Modify this code to return the correct layer version #
        lambda_layer_version = aws_lambda.LayerVersion.from_layer_version_arn(
            scope,
            id=f"ap-southeast-1-{self.python_version}-{package}-{layer_version}",
            layer_version_arn=f"arn:aws:lambda:ap-southeast-1:770693421928:layer:Klayers-p312-requests:3"
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
    
    def get_latest_layer_arns(self, region:str, python_version:str) -> dict:
        pass
        
    def construct_python_version(self, python_verion:str) -> str:
        pass