from aws_cdk import aws_lambda
from aws_cdk import App, Environment, Stack
from constructs import Construct

from cdk_klayers import Klayers
from cdk_klayers.exceptions import NoRegionProvidedError, KlayersError
import pytest

import jsii

class MockStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.klayers = Klayers(
            self,
            python_version = aws_lambda.Runtime.PYTHON_3_12
        )
    
    def layer_version(self, package, layer_version="latest"):
        return self.klayers.layer_version(self, package, layer_version)
    
    @Stack.environment.setter
    def environment(self, environment):
        self.environemnt = environment



app = App()
env_USA = Environment(region="us-west-2")
mock_stack = MockStack(app, "MyTestingStack", env=env_USA)
test_requests_layer = mock_stack.layer_version("requests", "latest")
layer_arn = test_requests_layer.layer_version_arn
print(layer_arn)
assert isinstance(test_requests_layer, jsii._reference_map.InterfaceDynamicProxy)

layer_arn = test_requests_layer.layer_version_arn
print(layer_arn)