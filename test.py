from aws_cdk import aws_lambda
from aws_cdk import App, Environment, Stack
from aws_cdk import Aws
from constructs import Construct

from cdk_klayers import Klayers
from cdk_klayers.exceptions import NoRegionProvidedError, KlayersError
import pytest

import jsii


class MockStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        powertools_layer = aws_lambda.LayerVersion.from_layer_version_arn(
            self,
            id="lambda-powertools",
            layer_version_arn=f"arn:aws:lambda:{Aws.REGION}:017000801446:layer:AWSLambdaPowertoolsPythonV2:69",
        )

        klayers = Klayers(
            self, python_version=aws_lambda.Runtime.PYTHON_3_12, region="ap-southeast-1"
        )

        self.requests_layer_version_3 = klayers.layer_version(self, "requests", "3")
        lambda_function = aws_lambda.Function(
            self,
            "HelloHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            code=aws_lambda.Code.from_asset("tests/lambda"),
            handler="hello.handler",
            layers=[self.requests_layer_version_3],
        )
        lambda_string = lambda_function.to_string()


app = App()
mock_stack = MockStack(app, "test")
print("break")
