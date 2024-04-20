from aws_cdk import aws_lambda
from aws_cdk import App, Environment, Stack
from constructs import Construct

from cdk_klayers import Klayers
from cdk_klayers.exceptions import NoRegionProvidedError, KlayersError
import pytest

import jsii
from tests.utils import validate_layer_arn

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

def test_create_no_region():
    app = App()
    with pytest.raises(KlayersError) as e:
        mock_stack = MockStack(app, "MyTestingStack")

    assert isinstance(e.value, NoRegionProvidedError)

def test_create():
    app = App()
    env_USA = Environment(region="us-west-2")
    mock_stack = MockStack(app, "MyTestingStack", env=env_USA)
    assert isinstance(mock_stack, Stack)
    
    test_requests_layer = mock_stack.layer_version("requests", "latest")
    assert isinstance(test_requests_layer, jsii._reference_map.InterfaceDynamicProxy)

    # Only a lambda layer has a layer_version_arn
    layer_arn = test_requests_layer.layer_version_arn
    assert validate_layer_arn(layer_arn)

    layer_name = layer_arn.split(":")[6]
    prefix,python_version,package = layer_name.split("-")
    assert prefix == "Klayers"
    assert python_version == aws_lambda.Runtime.PYTHON_3_12.to_string().replace("python", "p").replace(".","")
    assert package == "requests"

 
    

    