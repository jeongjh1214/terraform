#!/bin/python3

import sys
import boto3
import time, datetime

ec2 = boto3.client('ec2')

test = ec2.describe_instances(Filters=[{'Name':'instance-id', 'Values':['i-066fb0939cb16c46e']}])


print (test)
