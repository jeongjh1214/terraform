#!/bin/python3

import sys
import boto3
from botocore.exceptions import ClientError
from modules.holiday import holidaycheck

ec2 = boto3.client('ec2')

response = ec2.describe_regions()

a = [c['RegionName'] for c in response['Regions']] 
print (a)
