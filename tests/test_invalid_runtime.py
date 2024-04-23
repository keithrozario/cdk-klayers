from aws_cdk import aws_lambda
from aws_cdk import App, Stack
from constructs import Construct

from cdk_klayers import Klayers
from cdk_klayers.exceptions import InvalidPythonVersion, KlayersError
import pytest


class MockStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        klayers = Klayers(self, region="ap-southeast-1", python_version="python3.12")


def test_create_no_region():
    app = App()
    with pytest.raises(KlayersError) as e:
        mock_stack = MockStack(app, "MyTestingStack")

    assert isinstance(e.value, InvalidPythonVersion)
