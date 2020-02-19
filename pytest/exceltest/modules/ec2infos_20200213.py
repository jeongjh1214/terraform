#!/bin/python3

import sys
import boto3
import re
from botocore.exceptions import ClientError

def insidsplit(description):
    pattern = re.findall('^Created by CreateImage',description)
    if pattern:
        insid = description.split('CreateImage(')[1].split(')')[0]
        return (insid)
    
def systemTagcheck(tags):
    i = 0
    for a in tags:
        if a['Key'] == 'System':
            i += 1
    return (i)

def CreateTags(tag,snapshotid):
   snapshot = boto3.resource('ec2').Snapshot(snapshotid)
   tag = snapshot.create_tags(Tags=[{'Key':'System','Value':tag[0]}])


def instagcheck(instanceid):
    ec2 = boto3.client('ec2')
    ress = ec2.describe_tags(Filters=[{'Name' : 'resource-id', 'Values': [instanceid]}])
    instag = [i['Value'] for i in ress['Tags'] if i['Key'] == 'System']
    if instag:
        return (instag)

def tagcheckInsert(response):
    ec2 = boto3.client('ec2')
    for a in response['Snapshots']:
        volume = boto3.resource('ec2').Volume(a.get('VolumeId'))
        try:
            instanceid = instagcheck(volume.attachments[0]['InstanceId']) 
        except ClientError:
            instanceid = ''

        if instanceid:
            CreateTags(instanceid[0],a.get('SnapshotId'))
            print (("%s Tag를 %s SnapshotID에 입력하였습니다") %(instanceid[0], a.get('SnapshotId')))

def createSnapshotTag():
    ec2 = boto3.client('ec2')
    response = ec2.describe_snapshots(OwnerIds=['self'],MaxResults=1000)
    tagcheckInsert(response)

    while True: 
        try:
            ntoken = response['NextToken']
            ntoken = response['NextToken']
            response = ec2.describe_snapshots(OwnerIds=['self'],MaxResults=1000,NextToken=ntoken)
            tagcheckInsert(response)
        except KeyError:
            sys.exit()
        

def amiinscheck(abc):
    ec2 = boto3.client('ec2')
    response = ec2.describe_snapshots(OwnerIds=['self'],SnapshotIds=[abc])
    for i in response['Snapshots']:
        volume = boto3.resource('ec2').Volume(i.get('VolumeId'))
        try:
            return (instagcheck(volume.attachments[0]['InstanceId']))
        except ClientError:
            pass 

def amitagcreate():
    ec2 = boto3.client('ec2')
    ec2r = boto3.resource('ec2')
    response = ec2.describe_images(Owners=['self'])
    for i in response['Images']:
        for j in i['BlockDeviceMappings']:
            tag = amiinscheck(j['Ebs']['SnapshotId'])
            if tag:
                img = ec2r.Image(i['ImageId'])
                imgtag = img.create_tags(Tags=[{'Key': 'System', 'Value' : tag[0]}])
                print ("%s 이미지 태그 %s 등록하였습니다." %(i['ImageId'],imgtag))

def test():
    client = boto3.client('ec2')
    client2 = boto3.resource('ec2')
    response = client.describe_network_interfaces()
    
    for i in response['NetworkInterfaces']:
        try:
            
            if i['Attachment']:
                p = re.compile('[0-9]{12}')
                if i['Attachment']['InstanceOwnerId'] == 'amazon-aws':
                    pass

                elif i['Attachment']['InstanceOwnerId'] == 'amazon-rds':
                    tag = rdscheck(i['Groups'])
                    if tag:
                        test1 = client2.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tag}])

                elif i['Attachment']['InstanceOwnerId'] == 'amazon-elb':
                    tag = elbcheck(i['Groups'])
                    if tag:
                        test1 = client2.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tag}])
                    else:
                        tag1 = elbcheck2(i['Groups'])
                        if tag1:
                            test1 = client2.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tag1}])

                elif p.match(i['Attachment']['InstanceOwnerId']):
                    instag = instagcheck(i['Attachment']['InstanceId'])
                    if instag:
                        test1 = client2.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=[{'Key' : 'System', 'Value' : instag[0]}])
        except KeyError:
            pass
        
def rdscheck(groups):
    ec2 = boto3.client('rds')
    client = ec2.describe_db_instances()
    for i in client['DBInstances']:
        for j in i['VpcSecurityGroups']:
            for group in groups:
                if group['GroupId'] == j['VpcSecurityGroupId']:
                    cl = ec2.list_tags_for_resource(ResourceName=i['DBInstanceArn'])
                    tag = [a['Value'] for a in cl['TagList'] if a['Key'] == 'System']
                    if tag:
                        return (tag[0])

def elbcheck(groups):
    ec2 = boto3.client('elbv2')
    client = ec2.describe_load_balancers()
    for i in client['LoadBalancers']:
        try:
            for j in i['SecurityGroups']:
                for group in groups:
                    
                    if group['GroupId'] == j:
                        cl = ec2.describe_tags(ResourceArns=[i['LoadBalancerArn']])
                        tag = [a['Value'] for a in cl['TagDescriptions'][0]['Tags'] if a['Key'] == 'System']
                        
                        if tag:
                            return (tag[0])
        except KeyError:
            pass

def elbcheck2(groups):
    ec2 = boto3.client('elb')
    client = ec2.describe_load_balancers()
    for i in client['LoadBalancerDescriptions']:
        try:
            for j in i['SecurityGroups']:
                for group in groups:

                    if group['GroupId'] == j:
                        cl = ec2.describe_tags(LoadBalancerNames=[i['LoadBalancerName']])
                        
                        tag = [a['Value'] for a in cl['TagDescriptions'][0]['Tags'] if a['Key'] == 'System']
                        if tag:
                            return (tag[0])
        except KeyError:
            pass

def test1():
    ec2 = boto3.client('ec2')
    client = ec2.describe_security_groups()
    
    for i in client['SecurityGroups']:
        if i['GroupName'] == 'default':
            pass
        else:
            try:
                groupname = i['GroupId']
                groupid = {}
                groupid['GroupId'] = groupname
                client2 = boto3.resource('ec2')

                ecins = ec2.describe_instances(Filters=[{'Name':'network-interface.group-id', 'Values':[groupname]}])
                if ecins['Reservations']:
                    for k in ecins['Reservations']:
                        instance = [a['InstanceId'] for a in k['Instances']]
                        if instagcheck(instance[0]):
                            tag = instagcheck(instance[0])[0]
                            if tag:
                                test1 = client2.SecurityGroup(i['GroupId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tag}])
                                print (i['GroupId'],tag)
                    
                else:
                                                           
                    if rdscheck([groupid]):
                        tag = rdscheck([groupid])
                        if tag:
                            test1 = client2.SecurityGroup(i['GroupId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tag}])
                            print (i['GroupId'],tag)
                    elif elbcheck([groupid]):
                        tag = elbcheck([groupid])
                        if tag:
                            test1 = client2.SecurityGroup(i['GroupId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tag}])
                            print (i['GroupId'],tag)
                    elif elbcheck2([groupid]):
                        tag = elbcheck2([groupid])
                        if tag:
                            test1 = client2.SecurityGroup(i['GroupId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tag}])
                            print (i['GroupId'],tag)
            except KeyError:
                print (i['GroupId'] + " Key")
                pass


def tt():
    ec2 = boto3.client('rds')
    client = ec2.describe_db_snapshots()
    
    for i in client['DBSnapshots']:
        client2 = ec2.describe_db_instances(DBInstanceIdentifier=i['DBInstanceIdentifier'])
        resource = client2['DBInstances'][0]['DBInstanceArn']
        cl = ec2.list_tags_for_resource(ResourceName=resource)
        tag = [a['Value'] for a in cl['TagList'] if a['Key'] == 'System']
        
        if tag:
            test = ec2.add_tags_to_resource(ResourceName=i['DBSnapshotArn'],Tags=[{'Key' : 'System', 'Value' : tag[0]}])
            print (i['DBSnapshotArn'], tag[0])
tt()
#ec2 = boto3.resource('ec2')
#security_group = ec2.SecurityGroup('id')
#createSnapshotTag()
#amitagcreate()
#test()


