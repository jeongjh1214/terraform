#!/bin/python3

import boto3

ec2 = boto3.client('ec2')
#instances = [i for i in boto3.resource('ec2', region_name='eu-west-3').instances.all()]

#for i in instances:
#    print (i.instance_id)
#    print (i.tags)
