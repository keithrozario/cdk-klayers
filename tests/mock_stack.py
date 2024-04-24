from aws_cdk import aws_lambda
from aws_cdk import Stack
from constructs import Construct
from cdk_klayers import Klayers

class MockStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        global global_runtime
        self.klayers = Klayers(
            self,
            python_version = global_runtime
        )
    
    def layer_version(self, package, layer_version="latest"):
        return self.klayers.layer_version(self, package, layer_version)
    
    @Stack.environment.setter
    def environment(self, environment):
        self.environemnt = environment

class MockStackNoRegion(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.klayers = Klayers(
            self,
            python_version = aws_lambda.Runtime.PYTHON_3_12,
            region=kwargs['region']
        )
    
    def layer_version(self, package, layer_version="latest"):
        return self.klayers.layer_version(self, package, layer_version)
    
    @Stack.environment.setter
    def environment(self, environment):
        self.environemnt = environment
