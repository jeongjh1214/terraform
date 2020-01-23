#!/bin/python3

import boto3


ec2 = boto3.client('ec2')

def regions_list():
    regions = ['eu-north-1', 'ap-south-1', 'eu-west-3', 'eu-west-2', 'eu-west-1', 'ap-northeast-2', 'ap-northeast-1', 'sa-east-1', 'ca-central-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-central-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']

    return (regions)

#def instance_list(region):
#    allinstances = [i for i in boto3.resource('ec2', region_name=region).instances.all()] 
#    instances = []
#    for j in allinstances:
#        instances.append(j.instance_id)
#
#    a = {} 
#    if len(instances) != 0: 
#        a[region] = instances
#  
#    if len(a) != 0:
#        return (a)

def allinstance_list():
    allins = {} 
    for region in regions_list():
        allinstances = [i for i in boto3.resource('ec2', region_name=region).instances.all()] 
        instances = []
        for i in allinstances:
            instances.append((i.instance_id,i.state['Name']))

        if len(instances) != 0:
            allins[region] = instances

    return (allins)

def tag_check(InstanceId,region):
    ec2reg = boto3.client('ec2',region_name=region)
    response = ec2reg.describe_tags(Filters=[{'Name': 'resource-id','Values' : [InstanceId],},],)

    return (response['Tags'])

def fullname_check(InstanceId,region):
    response = tag_check(InstanceId,region)

    tags = [a for a in response if 'fullname' in a['Key']]

    if len(tags) == 0:
        return (False)
    else:
        return (response)


