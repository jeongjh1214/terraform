#!/bin/python3

import sys
import boto3
from botocore.exceptions import ClientError
from modules.holiday import holidaycheck

ec2 = boto3.client('ec2')

test = boto3.resource('ec2', region_name='ap-northeast-2').instances.all()

for i in test:
    print (i)
