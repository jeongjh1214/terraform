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
                'Values' : ['System']
            }
        ]
    )
    
    if len(astag['Tags']) == 0:
        return (False)

    asinfos = []
    for i in astag['Tags']:
        GroupName = i['ResourceId']
        #asinfo = client.describe_auto_scaling_groups(AutoScalingGroupNames=[GroupName])
        asinfo2 = client.describe_policies(AutoScalingGroupName=GroupName)
        #LaunchConfig = asinfo['AutoScalingGroups'][0]['LaunchConfigurationName']
        PolicyType = [a for a in asinfo2['ScalingPolicies'] if a['PolicyType'] == 'StepScaling']
        print (asinfo2['ScalingPolicies'])
        if len(PolicyType) > 0:
            for j in asinfo2['ScalingPolicies']:
                
                alarmName = j['Alarms'][0]['AlarmName']
                watchinfo = cloudwatchinfo(alarmName)
                if j['StepAdjustments'][0]['ScalingAdjustment'] > 0:
                    print ("abc")
                else:
                    print ("cde")
                
        #asinfos.append(asinfo2)
        #asinfos.append([GroupName,LaunchConfig])
    #print (asinfos[1]['ScalingPolicies'][0]['Alarms'])
    
    #for a in asinfos[1]['ScalingPolicies']:
    #    if a['StepAdjustments'][0]['StepAdjustments'] > 0:
    #        addserver = f"" 
    #return (asinfos[1]['ScalingPolicies'])

def elbtagcheck():
    client = boto3.client('elbv2')

    elbtags = client.describe_tags(
        ResourceArns=[
            'arn:aws:elasticloadbalancing:ap-northeast-2:779475221336:loadbalancer/net/nlb/69df28513080e0a9', 'arn:aws:elasticloadbalancing:ap-northeast-2:779475221336:loadbalancer/net/nlb-an2-ss-newrelic/aed9dd9a22dab032', 'arn:aws:elasticloadbalancing:ap-northeast-2:779475221336:loadbalancer/app/alb/d69fbe12db044ac5'
        ]
    )['TagDescriptions']

    return (elbtags)


def allelbArn():
    client = boto3.client('elbv2')

    elbinfos = client.describe_load_balancers()['LoadBalancers']
    elbArn = [i['LoadBalancerArn'] for i in elbinfos]
    return (elbArn)

def allelb():
    client = boto3.client('elbv2')

    elbinfos = client.describe_load_balancers()['LoadBalancers']
    
    return (elbinfos)
    
def test():
    client = boto3.client('elbv2')
    response = client.describe_listeners(
        LoadBalancerArn='arn:aws:elasticloadbalancing:ap-northeast-2:779475221336:loadbalancer/app/alb/d69fbe12db044ac5',
    )

    return (response)

def test1():
    client = boto3.client('elbv2')
    response = client.describe_target_health(
        TargetGroupArn='arn:aws:elasticloadbalancing:ap-northeast-2:779475221336:targetgroup/albtarget/d2d38a4426370a1d'
    )

    return (response)


def cloudwatchinfo(name):
    client = boto3.client('cloudwatch')
    response = client.describe_alarms(
        AlarmNames = [name]
    )

    for i in response['MetricAlarms']:
        return ([i['Statistic'],i['Period'],i['Threshold']])
    
print (asinfos('test'))
