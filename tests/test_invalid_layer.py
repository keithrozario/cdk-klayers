from aws_cdk import aws_lambda
from aws_cdk import App, Stack
from constructs import Construct

from cdk_klayers import Klayers
from cdk_klayers.exceptions import LayerNameDoesNotExists, KlayersError
import pytest


class MockStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        klayers = Klayers(
            self, python_version=aws_lambda.Runtime.PYTHON_3_12, region="ap-southeast-1"
        )
        bad_layer = klayers.layer_version(self, "bad-layer")


def test_create_no_region():
    app = App()
    with pytest.raises(KlayersError) as e:
        mock_stack = MockStack(app, "MyTestingStack")

    assert isinstance(e.value, LayerNameDoesNotExists)
