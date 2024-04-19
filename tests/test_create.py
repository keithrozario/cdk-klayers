from aws_cdk import aws_lambda
from aws_cdk import App, Environment, Stack
from constructs import Construct

from cdk_klayers import Klayers
from cdk_klayers.exceptions import NoRegionProvidedError, KlayersError
import pytest

class MockStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.klayers = Klayers(
            self,
            python_version = aws_lambda.Runtime.PYTHON_3_12,
            packages = ['idna', 'requests']
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
    env_USA = Environment(account="2383838383", region="us-west-2")
    mock_stack = MockStack(app, "MyTestingStack", env=env_USA)

    assert isinstance(mock_stack, Stack)