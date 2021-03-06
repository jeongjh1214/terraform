#!/bin/python3

import sys
import boto3
import re
import time
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
            print (f"{instanceid[0]} Tag를 {a.get('SnapshotId')} SnapshotID에 입력하였습니다")

def createSnapshotTag():
    starttime = time.time()
    ec2 = boto3.client('ec2')
    response = ec2.describe_snapshots(OwnerIds=['self'],MaxResults=1000)
    tagcheckInsert(response)

    print (time.time() - starttime)
    while True: 
        try:
            ntoken = response['NextToken']
            response = ec2.describe_snapshots(OwnerIds=['self'],MaxResults=1000,NextToken=ntoken)
            tagcheckInsert(response)
            print (time.time() - starttime)
            input("계속하시려면 Enter 를 눌러주세요")
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
                print (f"{i['ImageId']} 이미지 태그 {tag[0]} 등록하였습니다.") 




createSnapshotTag()
amitagcreate()
