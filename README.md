[![Python 3.10](https://img.shields.io/badge/python-3.10-green?style=for-the-badge)](https://www.python.org/downloads/release/python-3100/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-green?style=for-the-badge)](https://www.python.org/downloads/release/python-3110/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-green?style=for-the-badge)](https://www.python.org/downloads/release/python-3120/)  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000?style=for-the-badge)](https://github.com/psf/black)

# CDK-Klayers

Use [Klayers](https://github.com/keithrozario/Klayers) within your CDK Stacks.

## Install

    pip install cdk-klayers

## Usage (short version)

Simply use the Klayers Class within your CDK `Stack`. You will need to specify a runtime and region for it to work.

```python

from cdk_klayers import Klayers

class MockStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        runtime = aws_lambda.Runtime.PYTHON_3_12

        # Initialize Klayers 
        klayers = Klayers(
            self,
            python_version = runtime
            region = "ap-southeast-1"
        )
    
        # get the latest layer version for the requests package
        requests_layer = klayers.layer_version(self, "requests")

        lambda_function = aws_lambda.Function(
            self, 'HelloHandler',
            runtime=runtime,
            layers=[requests_layer],
            code=aws_lambda.Code.from_asset('lambda'),
            handler='hello.handler'
        )

```

## Usage (long version)

This example shows a fully working CDK stack that deploys a single lambda function with 2 layers from Klayers. The region of the stack was inferred from the CDK `Environment`.

```python

from aws_cdk import aws_lambda
from aws_cdk import App, Environment, Stack
from aws_cdk import Aws
from constructs import Construct

from cdk_klayers import Klayers

class MockStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        runtime = aws_lambda.Runtime.PYTHON_3_12

        # Initialize Klayers 
        klayers = Klayers(
            self,
            python_version = runtime
        )
    
        # get the latest layer version for the requests package
        requests_layer = klayers.layer_version(self, "requests")
        idna_layer = klayers.layer_version(self, "idna", layer_version="2")

        lambda_function = aws_lambda.Function(
            self, 'HelloHandler',
            runtime=runtime,
            layers=[requests_layer, idna_layer],
            code=aws_lambda.Code.from_asset('lambda'),
            handler='hello.handler'
        )


app = App()
env = Environment(region="us-east-1")
mock_stack =MockStack(app, "test", env=env)
```

## Other Notes

We're still in beta, this might change. Please raise an issue if you have any feedback.
