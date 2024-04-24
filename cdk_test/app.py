#!/usr/bin/env python3
import os
import sys
from pathlib import Path

from cdk_test.cdk_test_stack import CdkTestStack

from aws_cdk import aws_lambda
from aws_cdk import App, Stack, Environment
from aws_cdk import Aws
from constructs import Construct

sys.path.append(str(Path(os.getcwd()).parent))
from cdk_klayers import Klayers


class MockStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        powertools_layer = aws_lambda.LayerVersion.from_layer_version_arn(
            self,
            id="lambda-powertools",
            layer_version_arn=f"arn:aws:lambda:{Aws.REGION}:017000801446:layer:AWSLambdaPowertoolsPythonV2:69",
        )

        klayers = Klayers(self, python_version=aws_lambda.Runtime.PYTHON_3_12)

        idna_layer = klayers.layer_version(self, "requests")
        requests_layer = klayers.layer_version(self, "idna")
        xray_layer = klayers.layer_version(self, "aws-xray-sdk", layer_version="1")
        lambda_function = aws_lambda.Function(
            self,
            "HelloHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            code=aws_lambda.Code.from_asset("lambda"),
            handler="hello.handler",
            layers=[idna_layer, requests_layer, xray_layer],
        )


app = App()
env = Environment(region="ap-southeast-1")
mock_stack = MockStack(app, "test", env=env)
app.synth()
