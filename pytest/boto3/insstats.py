#!/bin/python3

import sys
import boto3
from botocore.exceptions import ClientError
from modules.holiday import holidaycheck

ec2 = boto3.client('ec2')
instances = [i for i in boto3.resource('ec2', region_name='ap-northeast-2').instances.all()]

action = sys.argv[1].lower() 


if holidaycheck() == 0:
    for i in instances:
        if action == 'on':
            try:
                ec2.start_instances(InstanceIds=[i.instance_id], DryRun=True)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise
            try:
                response = ec2.start_instances(InstanceIds=[i.instance_id], DryRun=False)
                print (response)
            except ClientError as e:
                print (e)
    
        elif action == 'off':
            try:
                ec2.stop_instances(InstanceIds=[i.instance_id], DryRun=True)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise
            try:
                response = ec2.stop_instances(InstanceIds=[i.instance_id], DryRun=False)
                print (response)
            except ClientError as e:
                print (e)

else:
    sys.exit()

