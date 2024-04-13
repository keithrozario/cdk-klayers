from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda,
)
from aws_cdk import Aws

# Because of the way cdk synth works, we'll need to hardcode this for now.
# will figure out relative imports later....
import sys
sys.path.append("/Users/krozario/projects/cdk-klayers/cdk-klayers")
from cdk_klayers import Klayers

class CdkPythonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        klayers = Klayers(
            python_version = aws_lambda.Runtime.PYTHON_3_12,
            region= Aws.REGION
        )

        lambda_function = aws_lambda.Function(
            self, 'HelloHandler',
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            code=aws_lambda.Code.from_asset('lambda'),
            handler='hello.handler',
            layers=[
                klayers.layer_version(
                    self,
                    package="requests"
                    )
            ]
        )

        # lambda_function_2 = aws_lambda.Function(
        #     self, 'GoodbyeHandler',
        #     runtime=aws_lambda.Runtime.PYTHON_3_12,
        #     code=aws_lambda.Code.from_asset('lambda'),
        #     handler='hello.handler',
        #     layers=[cdk_klayers.get_layers(
        #         self,
        #         region="ap-southeast-1",
        #         package="requests",
        #         python_version=aws_lambda.Runtime.PYTHON_3_12,
        #     )]
        # )