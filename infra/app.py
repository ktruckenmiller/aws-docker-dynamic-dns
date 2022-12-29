#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infra.infra_stack import InfraStack


app = cdk.App()
InfraStack(
    app, "dynamic-dns", env=cdk.Environment(account="601394826940", region="us-west-2")
)

app.synth()
