from aws_cdk import aws_lambda
from aws_cdk import App, Stack
from constructs import Construct

from cdk_klayers import Klayers

import jsii
from tests.utils import validate_layer_arn


class MockStackHardCodeConfig(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        klayers = Klayers(
            self,
            python_version = aws_lambda.Runtime.PYTHON_3_12,
            region = "ap-southeast-1"
        )
    
        self.requests_layer_version_3 = klayers.layer_version(self, "requests", "3")
        self.idna_layer = klayers.layer_version(self, "idna")

        self.lambda_function = aws_lambda.Function(
            self, 'HelloHandler',
            runtime= aws_lambda.Runtime.PYTHON_3_12,
            code=aws_lambda.Code.from_asset('lambda'),
            handler='hello.handler',
            layers=[self.requests_layer_version_3]
        )

        self.lambda_function.add_layers(self.idna_layer)


def test_stack_create():

    app = App()

    mock_stack = MockStackHardCodeConfig(app, "MyTestingStack")
    assert isinstance(mock_stack, Stack)
    
    test_requests_layer = mock_stack.requests_layer_version_3
    assert isinstance(test_requests_layer, jsii._reference_map.InterfaceDynamicProxy)
    
    layer_arn = test_requests_layer.layer_version_arn
    assert validate_layer_arn(layer_arn)

    layer_name = layer_arn.split(":")[6]
    prefix,python_version,*layer_package = layer_name.split("-")
    # Python packages can also have dashes(-) in the name
    layer_package_name = '-'.join(layer_package)
    
    assert prefix == "Klayers"
    assert python_version == "p312"
    assert layer_package_name == "requests"

    layer_region = layer_arn.split(":")[3]
    assert layer_region == "ap-southeast-1"
