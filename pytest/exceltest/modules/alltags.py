#!/bin/python3

import sys
import boto3
from botocore.exceptions import ClientError

def Alltags():
    client = boto3.resource('ec2')

    Alltags = {}
       
    for instance in client.instances.filter(MaxResults=500):
        try:
            SystemTag = list(filter(lambda tag: tag['Key'] == 'System', instance.tags))[0]['Value']
            InsTags = list(filter(lambda tag: tag['Key'] == 'System' or tag['Key'] == 'Company' or tag['Key'] == 'Country' or tag['Key'] == 'STAGE', instance.tags))
            
            Alltags[SystemTag] = InsTags 

        except IndexError:
            print (str(instance) + ' IndexError')
            pass
        except TypeError:
            print (str(instance) + ' TypeError')
    
    return (Alltags)

def volumtagging():
    alltags = Alltags()
    ec2 = boto3.client('ec2')
    volume = ec2.describe_volumes()
    for i in volume['Volumes']:
        if i['State'] == 'in-use':
            ec2res = boto3.resource('ec2')
            try:
                volumeres = [a['Value'] for a in ec2res.Volume(i['VolumeId']).tags if a['Key'] == 'System']
            except TypeError:
                volumeres = None
            
            if volumeres:
                try:
                    systemcheck = alltags[volumeres[0]]
                except KeyError:
                    print (f"{i['VolumeId']} 볼륨 System 태그 {volumeres[0]} 와 매칭되는 System 키가 없습니다")
                    systemcheck = None

                if systemcheck:
                    ec2res.Volume(i['VolumeId']).create_tags(Tags=systemcheck)
                    
                
def securitytagging():
    alltags = Alltags()
    ec2 = boto3.client('ec2')
    client = ec2.describe_security_groups()

    for i in client['SecurityGroups']:
        ec2res = boto3.resource('ec2')
        try:
            sgres = [a['Value'] for a in ec2res.SecurityGroup(i['GroupId']).tags if a['Key'] == 'System']
        except TypeError:
            sgres = None

        if sgres:
            try:
                systemcheck = alltags[sgres[0]]
            except KeyError:
                    print (f"{i['GroupId']} SG System 태그 {sgres[0]} 와 매칭되는 System 키가 없습니다")
                    systemcheck = None

            if systemcheck:
                ec2res.SecurityGroup(i['GroupId']).create_tags(Tags=systemcheck)


def networktagging():
    alltags = Alltags()
    ec2 = boto3.client('ec2')
    client = ec2.describe_network_interfaces()

    for i in client['NetworkInterfaces']:
        
        ec2res = boto3.resource('ec2')
        try:
            netres = [a['Value'] for a in ec2res.NetworkInterface(i['NetworkInterfaceId']).tag_set if a['Key'] == 'System']
                        
        except TypeError:
            netres = None

        if netres:
            try:
                systemcheck = alltags[netres[0]]
            except KeyError:
                    print (f"{i['NetworkInterfaceId']} ENI System 태그 {netres[0]} 와 매칭되는 System 키가 없습니다")
                    systemcheck = None

            if systemcheck:
                ec2res.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=systemcheck)

def elbtagging():
    alltags = Alltags()
    ec2 = boto3.client('elb')
    client = ec2.describe_load_balancers()

    for i in client['LoadBalancerDescriptions']:
        try:
            elbres = [a['Value'] for a in ec2.describe_tags(LoadBalancerNames=[i['LoadBalancerName']])['TagDescriptions'][0]['Tags'] if a['Key'] == 'System']
                             
        except TypeError:
            elbres = None

        if elbres:
            try:
                systemcheck = alltags[elbres[0]]
            except KeyError:
                    print (f"{i['LoadBalancerName']} ELB2 System 태그 {elbres[0]} 와 매칭되는 System 키가 없습니다")
                    systemcheck = None

            if systemcheck:
                ec2.add_tags(LoadBalancerNames=[i['LoadBalancerName']],Tags=systemcheck)

def elb2tagging():
    alltags = Alltags()
    ec2 = boto3.client('elbv2')
    client = ec2.describe_load_balancers()

    for i in client['LoadBalancers']:
        try:
            elb2res = [a['Value'] for a in ec2.describe_tags(ResourceArns=[i['LoadBalancerArn']])['TagDescriptions'][0]['Tags'] if a['Key'] == 'System']
                             
        except TypeError:
            elb2res = None

        if elb2res:
            try:
                systemcheck = alltags[elb2res[0]]
            except KeyError:
                    print (f"{i['LoadBalancerArn']} ELB2 System 태그 {elb2res[0]} 와 매칭되는 System 키가 없습니다")
                    systemcheck = None

            if systemcheck:
                ec2.add_tags(ResourceArns=[i['LoadBalancerArn']],Tags=systemcheck)
    
def autoscatagging():
    client = boto3.client('autoscaling')

    print (client.describe_auto_scaling_groups())

def test():
    client = boto3.client('apigateway')
    test = client.tag_resource(
        resourceArn='arn:aws:apigateway:ap-northeast-2::/restapis/7y3a2v6eae',
        tags={'test' : 'system','abc':'abc'}
    )
    for i in client.get_rest_apis()['items']:
        print (i['id'])
    #print (test1)

def test1():
    client = boto3.client('ec2')
    aa = client.describe_subnets()
    for i in aa['Subnets']:
        subnetid = i['SubnetId']
        boto3.resource('ec2').Subnet(subnetid).create_tags(Tags=[{'Key' : 'Company', 'Value': 'AP'},{'Key' : 'Service', 'Value' :''}])
        sys.exit()
test1()