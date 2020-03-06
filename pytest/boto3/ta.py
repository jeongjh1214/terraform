#!/bin/python3

import sys
import boto3
from botocore.exceptions import ClientError
import re, datetime
from dateutil.relativedelta import relativedelta

#ec2 = boto3.client('ec2')
#response = ec2.deregister_image(ImageId='ami-0aa6b4fd28c0ab28d')
#
#print (response)

client = boto3.client('glue')
arn = "arn:aws:glue:ap-northeast-2:779475221336:workflow/test"
t = client.list_workflows()
tt = client.tag_resource(ResourceArn=arn,TagsToAdd={'System':'test'})

print (tt)
