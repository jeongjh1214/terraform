#!/bin/python3

import sys
import boto3
from botocore.exceptions import ClientError

client = boto3.resource('ec2')

instances = client.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

for i in instances:
    instance_name = list(filter(lambda tag: tag['Key'] == 'Name', i.tags))[0]['Value']
    print (i.tags)

