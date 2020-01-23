#!/bin/python3

import boto3
import datetime
from botocore.exceptions import ClientError
from modules.holiday import holidaycheck
from pytz import timezone

ec2 = boto3.client('ec2')
instances = [i for i in boto3.resource('ec2', region_name='ap-northeast-2').instances.all()]

now_utc = datetime.datetime.now(timezone('UTC'))
now_kst = now_utc.astimezone(timezone('Asia/Seoul'))

def instance_start():
    for i in instances:
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

def instance_stop():
    for i in instances:
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

def lambda_handler (event, context):
    if now_kst.strftime("%H") == '09' and holidaycheck() == 0:
        instance_start()
    if now_kst.strftime("%H") == '19' and holidaycheck() == 0:
        instance_stop()


if now_kst.strftime("%H") == '09' and holidaycheck() == '0':
    print ("abc")
if now_kst.strftime("%H") == '19' and holidaycheck() == 0:
    print ("def")
