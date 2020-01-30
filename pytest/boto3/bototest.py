#!/bin/python3

import sys
import boto3
from botocore.exceptions import ClientError
from modules.holiday import holidaycheck

client = boto3.client('elbv2')

response = client.describe_listeners(
    ListenerArns=[
        'arn:aws:elasticloadbalancing:ap-northeast-2:584946075280:listener/app/test/6128197d9dabd7c7/8fe4383c24dc1d92',
    ],
)

response1 = client.describe_rules(
    RuleArns=[
        'arn:aws:elasticloadbalancing:ap-northeast-2:584946075280:listener-rule/app/test/6128197d9dabd7c7/8fe4383c24dc1d92/72796f3a29d2664d',
    ],
)

print (response1)
            
