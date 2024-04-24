# CDK-Klayers

Python package for using [Klayers](https://github.com/keithrozario/Klayers) within your CDK Stacks.

 [![Python 3.12](https://img.shields.io/badge/python-3.12-green?style=for-the-badge)](https://www.python.org/downloads/release/python-3120/)  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000?style=for-the-badge)](https://github.com/psf/black)

## Install

    pip install cdk-klayers

## Usage

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
        idna_layer = klayers.layer_version(self, "idna")

        lambda_function = aws_lambda.Function(
            self, 'HelloHandler',
            runtime=runtime,
            layers=[requests_layer, idna_layer],
            code=aws_lambda.Code.from_asset('lambda'),
            handler='hello.handler'
            # other props
        )


app = App()
env = Environment(region="us-east-1")
mock_stack =MockStack(app, "test", env=env)
```

## Other Notes

We're still in beta. Currently we've only tested in Python 3.12, but will extend support for python 3.11, and python 3.10 soon as well.