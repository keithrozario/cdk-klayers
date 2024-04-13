#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_stack import CdkPythonStack

app = cdk.App()
CdkPythonStack(app, "CdkPythonStack")

app.synth()