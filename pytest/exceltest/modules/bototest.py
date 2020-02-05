#!/bin/python3

import sys
import boto3
from botocore.exceptions import ClientError

def alltags():
    client = boto3.client('ec2')

    alltags = []

    for i in client.describe_tags()['Tags']:
        if i['Key'] == 'Name' and i['ResourceType'] == 'instance':
            alltags.append(i['Value'])

    return (list(set(alltags)))

def ec2infos(regions,systemTags):
    
    ec2 = boto3.resource('ec2', regions)

    filters = [
        {
            'Name' : 'tag:Name',
            'Values' : [systemTags]
        }
    ]

    instances = ec2.instances.filter(Filters=filters)

    #instanceinfos = [i.instance_type for i in instances]
    
    ####인스턴스 아이디
    #return (instanceinfos)
    a = []
    for i in instances:
        a.append(i.instance_type)
    return (a)

print (ec2infos('ap-northeast-2','ec2-an2-jaehoon-test-2c'))
