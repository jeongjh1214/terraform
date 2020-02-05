#!/bin/python3

import sys
import boto3
from botocore.exceptions import ClientError

client = boto3.client('ec2')

for i in client.describe_tags()['Tags']:
    if i['Key'] == 'Name':
        print (i)
