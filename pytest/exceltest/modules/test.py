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
        if not a.get('Tags'):
            instanceid = insidsplit(a['Description']) 
            if instanceid:
                inschk = instagcheck(instanceid)
                if inschk:
                    CreateTags(inschk[0],a.get('SnapshotId'))
                    print (("%s Tag를 %s SnapshotID에 입력하였습니다") %(inschk[0], a.get('SnapshotId')))
                else:
                    pass
        else:
            if systemTagcheck(a.get('Tags')) > 1:
                pass
            else:
                instanceid = insidsplit(a['Description']) 
                if instanceid:
                    inschk = instagcheck(instanceid)
                    if inschk:
                        CreateTags(inschk[0],a.get('SnapshotId'))
                        print (("%s Tag를 %s SnapshotID에 입력하였습니다") %(inschk[0], a.get('SnapshotId')))
                else:
                    pass


def createSnapshotTag():
    ec2 = boto3.client('ec2')
    response = ec2.describe_snapshots(OwnerIds=['self'],MaxResults=100)
    tagcheckInsert(response)

    while True: 
        ntoken = response['NextToken']
        response = ec2.describe_snapshots(OwnerIds=['self'],MaxResults=100,NextToken=ntoken)
        tagcheckInsert(response)
        try:
            test = response['NextToken']
            input("계속하시려면 Enter 를 눌러주세요")
        except KeyError:
            sys.exit()
        

def test():
    ec2 = boto3.client('ec2')
    response = ec2.describe_snapshots(OwnerIds=['self'],MaxResults=100)
    for i in response['Snapshots']:
        volume = boto3.resource('ec2').Volume(i.get('VolumeId'))
        try:
            print (instagcheck(volume.attachments[0]['InstanceId']))
        except ClientError:
            print ("abc")
#createSnapshotTag()

test()
