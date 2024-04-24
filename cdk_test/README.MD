# CDK-Test

This directory is to an end-2-end test within a CDK `synth` process. The magic is here:

```python
sys.path.append(str(Path(os.getcwd()).parent))
from cdk_klayers import Klayers
```

Where we add the top level directory into the PYTHONPATH, and hence python can import the cdk_klayers directly from the top level directory.

The test should create lambda function with the following 3 layers, in ap-southeast-1:

Layers:
        - arn:aws:lambda:ap-southeast-1:770693421928:layer:Klayers-p312-aws-xray-sdk:1
        - arn:aws:lambda:ap-southeast-1:770693421928:layer:Klayers-p312-idna:1
        - arn:aws:lambda:ap-southeast-1:770693421928:layer:Klayers-p312-requests:3

aws-xray-sdk will always be version 1 (as we request that). The other 2 layers will change version depending on what's the latest available.


## Run Test

    $ cdk synth

