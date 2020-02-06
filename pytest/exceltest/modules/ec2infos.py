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

def volumecheck(volid):
    ec2 = boto3.resource('ec2')
    allsize = []
    
    for i in volid:
        volume = ec2.Volume(i)
        allsize.append(volume.size)

    allsize.sort()

    ebsinfo = {}
    
    if len(allsize) == 1:
        ebsinfo['root'] = allsize[0]
        ebsinfo['data'] = ''
        ebsinfo['swap'] = ''

    elif len(allsize) == 2:
        ebsinfo['root'] = allsize[0]
        ebsinfo['data'] = allsize[1]
        ebsinfo['swap'] = ''

    elif len(allsize) == 3:
        ebsinfo['root'] = allsize[1]
        ebsinfo['swap'] = allsize[0]
        ebsinfo['data'] = allsize[2]
    
    elif len(allsize) > 3:
        ebsinfo['root'] = allsize[1]
        ebsinfo['swap'] = allsize[0]
        ebsinfo['data'] = allsize[2:-1]

    return (ebsinfo)

#def vpctest(vpcid):
#    ec2 = boto3.resource('ec2')
#    vpc = ec2.Vpc(vpcid)
#    #return (vpc.subnets.all())
#    a = [i.cidr_block for i in vpc.subnets.all()]
#    return (a)


def ec2infos(regions,systemTags):
    
    ec2 = boto3.resource('ec2', regions)

    filters = [
        {
            'Name' : 'tag:Name',
            'Values' : [systemTags]
        }
    ]
    
    instances = ec2.instances.filter(Filters=filters)

    # No, 환경, 지역, Hostname, AMI, Instance Type, Private IP, Root Volume(GB), IAM role, Data Volume(GB), Swap Space(GB)
    
    ## 인스턴스 아이디
    
    allinsinfo = []
    ec2num = 0

    for i in instances:
        ec2num += 1

        ec2env = ''
        # 환경 및 호스트네임        
        for j in i.tags:
            if j['Key'] == 'STAGE':
                ec2env = j['Value']
            elif j['Key'] == 'Name':
                ec2name = j['Value']

        
        vollist = [ebs['Ebs']['VolumeId'] for ebs in i.block_device_mappings]
        volsizelist = volumecheck(vollist)

        if i.iam_instance_profile:
            iamrole = i.iam_instance_profile['Arn'].split('/')[-1]
        else:
            iamrole = ''            

        ec2info = [ec2num,ec2env,regions,ec2name,'',i.instance_type,i.private_ip_address,volsizelist['root'],iamrole,volsizelist['data'],volsizelist['swap']]
        allinsinfo.append(ec2info)
            
    return (allinsinfo)

def asinfos(tag):
    client = boto3.client('autoscaling')
    
    astag = client.describe_tags(
        Filters=[
            {
                'Name' : 'value',
                'Values' : [tag]
            },
            {
                'Name' : 'key',
                'Values' : ['system']
            }
        ]
    )
    
    if len(astag['Tags']) == 0:
        return (False)

    asinfos = []
    for i in astag['Tags']:
        GroupName = i['ResourceId']
        asinfo = client.describe_auto_scaling_groups(AutoScalingGroupNames=[GroupName])
        LaunchConfig = asinfo['AutoScalingGroups'][0]['LaunchConfigurationName']
        asinfos.append([GroupName,LaunchConfig])
            
    return (asinfos)