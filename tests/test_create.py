from aws_cdk import aws_lambda
from aws_cdk import App, Environment, Stack
from constructs import Construct

from cdk_klayers import Klayers

import jsii
from tests.utils import validate_layer_arn

global_runtime = aws_lambda.Runtime.PYTHON_3_12


class MockStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        global global_runtime
        self.klayers = Klayers(self, python_version=global_runtime)

    def layer_version(self, package, layer_version="latest"):
        return self.klayers.layer_version(self, package, layer_version)


def mock_stack_create(region: str, package: str, runtime: aws_lambda.Runtime):

    app = App()
    env = Environment(region=region)

    #  not the best approach, but I needed to pass runtime to the Class
    #  and could not use the constructor.
    global global_runtime
    global_runtime = runtime

    mock_stack = MockStack(app, "MyTestingStack", env=env)
    assert isinstance(mock_stack, Stack)

    test_layer = mock_stack.layer_version(package, "latest")
    assert isinstance(test_layer, jsii._reference_map.InterfaceDynamicProxy)

    # Only a lambda layer has a layer_version_arn
    layer_arn = test_layer.layer_version_arn
    assert validate_layer_arn(layer_arn)

    layer_name = layer_arn.split(":")[6]
    prefix, python_version, *layer_package = layer_name.split("-")
    # Python packages can also have dashes(-) in the name
    layer_package_name = "-".join(layer_package)

    assert prefix == "Klayers"
    assert python_version == runtime.to_string().replace("python", "p").replace(".", "")
    assert layer_package_name == package

    layer_region = layer_arn.split(":")[3]
    assert layer_region == region


def test_python_312():
    mock_stack_create(
        region="ap-southeast-1", package="idna", runtime=aws_lambda.Runtime.PYTHON_3_12
    )


def test_python_311():
    mock_stack_create(
        region="us-east-1", package="requests", runtime=aws_lambda.Runtime.PYTHON_3_11
    )


def test_python_310():
    mock_stack_create(
        region="ap-southeast-3",
        package="aws-xray-sdk",
        runtime=aws_lambda.Runtime.PYTHON_3_10,
    )
