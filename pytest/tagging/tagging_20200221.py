#!/bin/python3

import sys
import boto3
import re
import time
from botocore.exceptions import ClientError


#region = 'ap-northeast-2'
#region = 'us-east-1'
#region = 'ap-northeast-1'
#region = 'eu-west-3'
#region = 'ap-southeast-1'



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
   snapshot = boto3.resource('ec2', region_name=region).Snapshot(snapshotid)
   tag = snapshot.create_tags(Tags=[{'Key':'System','Value':tag}])

def instagcheck(instanceid):
    ec2 = boto3.client('ec2',region_name=region)
    ress = ec2.describe_tags(Filters=[{'Name' : 'resource-id', 'Values': [instanceid]}])
    instag = [i['Value'] for i in ress['Tags'] if i['Key'] == 'System']
    if instag:
        return (instag)

def tagcheckInsert(response):
    ec2res = boto3.resource('ec2')

    for i in response['Snapshots']:
        # System Tag 
        try:
            tagcheck = [a for a in i['Tags'] if a['Key'] == 'System']
        except KeyError:
            tagcheck = None

        if tagcheck:
            pass
        else:
            try:
                volume = ec2res.Volume(i.get('VolumeId'))
                insid = volume.attachments[0]['InstanceId']

            except ClientError:
                print (f"볼륨명 {i.get('VolumeId')} 가 없습니다")
                insid = None

            except KeyError:
                print (f"{i.get('SnapshotId')}의 Instance 가 없습니다")
                insid = None

            if insid:
                tag = InsTags(insid)
                if tag:
                    tagging = ec2res.Snapshot(i.get('SnapshotId')).create_tags(Tags=tag)
                    print (f"{insid}를 {i.get('SnapshotId')}에 입력하였습니다")


def createSnapshotTag():
    ec2 = boto3.client('ec2',region_name=region)
    response = ec2.describe_snapshots(OwnerIds=['self'],MaxResults=500)
    tagcheckInsert(response)

    while True: 
        try:
            ntoken = response['NextToken']
            response = ec2.describe_snapshots(OwnerIds=['self'],MaxResults=500,NextToken=ntoken)
            tagcheckInsert(response)

        except KeyError:
            sys.exit()

def amiinscheck(abc):
    ec2 = boto3.client('ec2',region_name=region)
    response = ec2.describe_snapshots(OwnerIds=['self'],SnapshotIds=[abc])

    for i in response['Snapshots']:
        volume = boto3.resource('ec2',region_name=region).Volume(i.get('VolumeId'))
        try:
            return (instagcheck(volume.attachments[0]['InstanceId']))
        except ClientError:
            pass 

def amitagcreate():
    ec2 = boto3.client('ec2',region_name=region)
    ec2r = boto3.resource('ec2',region_name=region)
    response = ec2.describe_images(Owners=['self'])

    for i in response['Images']:
        for j in i['BlockDeviceMappings']:
            tag = amiinscheck(j['Ebs']['SnapshotId'])
            if tag:
                img = ec2r.Image(i['ImageId'])
                imgtag = img.create_tags(Tags=[{'Key': 'System', 'Value' : tag[0]}])
                print ("%s 이미지 태그 %s 등록하였습니다." %(i['ImageId'],imgtag))

def enitagcreate(clenv):
    client = boto3.client('ec2',region_name=region)
    client2 = boto3.resource('ec2',region_name=region)
    response = client.describe_network_interfaces()

    for i in response['NetworkInterfaces']:
        try:
            if i['Attachment']:
                p = re.compile('[0-9]{12}')

                if i['Attachment']['InstanceOwnerId'] == 'amazon-rds':
                    tag = rdscheck(i['Groups'])
                    if tag:
                        test1 = client2.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tag}])
                        print ("%s eni 태그 %s 등록하였습니다" %(i['NetworkInterfaceId'],tag))

                elif i['Attachment']['InstanceOwnerId'] == 'amazon-elb':
                    tag = elbcheck(i['Groups'])
                    if tag:
                        test1 = client2.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tag}])
                        print ("%s eni 태그 %s 등록하였습니다" %(i['NetworkInterfaceId'],tag))

                    else:
                        tag1 = elbcheck2(i['Groups'])
                        if tag1:
                            test1 = client2.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tag1}])
                            print ("%s eni 태그 %s 등록하였습니다" %(i['NetworkInterfaceId'],tag1))

                elif p.match(i['Attachment']['InstanceOwnerId']):
                    instag = instagcheck(i['Attachment']['InstanceId'])
                    if instag:
                        test1 = client2.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=[{'Key' : 'System', 'Value' : instag[0]}])
                        print ("%s eni 태그 %s 등록하였습니다" %(i['NetworkInterfaceId'],instag[0]))

                else:
                    tag = "Resource-ENI " + clenv
                    test1 = client2.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tag}])
                    print ("%s eni 태그 %s 등록하였습니다" %(i['NetworkInterfaceId'],tag))

            else:
                tag = "Resource-ENI " + clenv
                test1 = client2.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tag}])
                print ("%s eni 태그 %s 등록하였습니다" %(i['NetworkInterfaceId'],tag))
               
        except KeyError:
            pass

def test():
    volume = boto3.resource('ec2',region_name=region).Volume('vol-0ff5e76f5dd168d64')
    try:
        instanceid = instagcheck(volume.attachments[0]['InstanceId']) 
    except ClientError:
        instanceid = None

    return (instanceid) 

def rdscheck(groups):
    ec2 = boto3.client('rds',region_name=region)
    client = ec2.describe_db_instances()
    for i in client['DBInstances']:
        for j in i['VpcSecurityGroups']:
            for group in groups:
                if group['GroupId'] == j['VpcSecurityGroupId']:
                    cl = ec2.list_tags_for_resource(ResourceName=i['DBInstanceArn'])
                    tag = list(filter(lambda tag: tag['Key'] == 'System' or tag['Key'] == 'Company' or tag['Key'] == 'Country' or tag['Key'] == 'STAGE', cl['TagList']))
                    
                    if tag:
                        return (tag)

def elbcheck(groups):
    ec2 = boto3.client('elbv2')
    client = ec2.describe_load_balancers()
    for i in client['LoadBalancers']:
        try:
            for j in i['SecurityGroups']:
                for group in groups:
                    if group['GroupId'] == j:
                        cl = ec2.describe_tags(ResourceArns=[i['LoadBalancerArn']])
                        tag = list(filter(lambda tag: tag['Key'] == 'System' or tag['Key'] == 'Company' or tag['Key'] == 'Country' or tag['Key'] == 'STAGE', cl['TagDescriptions'][0]['Tags']))
                        
                        if tag:
                            return (tag)
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
                        tag = list(filter(lambda tag: tag['Key'] == 'System' or tag['Key'] == 'Company' or tag['Key'] == 'Country' or tag['Key'] == 'STAGE', cl['TagDescriptions'][0]['Tags']))
                        
                        if tag:
                            return (tag)
        except KeyError:
            pass

def sgtagging(clenv):
    ec2 = boto3.client('ec2',region_name=region)
    client = ec2.describe_security_groups()
    
    for i in client['SecurityGroups']:
        if i['GroupName'] == 'default':
            pass
        else:
            try:
                groupname = i['GroupId']
                groupid = {}
                groupid['GroupId'] = groupname
                client2 = boto3.resource('ec2',region_name=region)
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
                        
                    elif elbcheck([groupid]):
                        tag = elbcheck([groupid])
                        
                    elif elbcheck2([groupid]):
                        tag = elbcheck2([groupid])
                        
                    if tag:
                            test1 = client2.SecurityGroup(i['GroupId']).create_tags(Tags=tag)
                            print (i['GroupId'],tag)
                    else:
                        tag = 'Resource-SG ' + clenv
                        test1 = client2.SecurityGroup(i['GroupId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tag}])
                        print (i['GroupId'],tag)
            
            except KeyError:
                print (i['GroupId'] + " KeyError")
                pass

def rdstagcheck(response):
    ec2 = boto3.client('rds')
    for i in response['DBSnapshots']:
        if i['DBInstanceIdentifier']:
            tagcheck = [a for a in ec2.list_tags_for_resource(ResourceName=i['DBSnapshotArn'])['TagList'] if a['Key'] == 'System']
            if tagcheck:
                tagcheck = None
                continue
            else:
                try:
                    res = ec2.describe_db_instances(DBInstanceIdentifier=i['DBInstanceIdentifier'])
                    if res['DBInstances']:
                        resource = res['DBInstances'][0]['DBInstanceArn']
                        cl = ec2.list_tags_for_resource(ResourceName=resource)
                        tag = list(filter(lambda tag: tag['Key'] == 'System' or tag['Key'] == 'Company' or tag['Key'] == 'Country' or tag['Key'] == 'STAGE', cl['TagList']))
                        
                        if tag:
                            tagging = ec2.add_tags_to_resource(ResourceName=i['DBSnapshotArn'],Tags=tag)
                            print (f"{i['DBSnapshotArn']}에 {tag} 등록 완료하였습니다")
            
                except ClientError:
                    pass    

def rdssnapshot():
    ec2 = boto3.client('rds')
    response = ec2.describe_db_snapshots(MaxRecords=100)
    rdstagcheck(response)
    
    while True:
        try:
            marker = client['Marker']
            response = ec2.describe_db_snapshots(Marker=marker,MaxRecords=100)
            rdstagcheck(response)
        except KeyError:
            sys.exit()

def Alltags():
    client = boto3.resource('ec2',region_name=region)
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
    ec2 = boto3.client('ec2',region_name=region)
    volume = ec2.describe_volumes()
    for i in volume['Volumes']:
        if i['State'] == 'in-use':
            ec2res = boto3.resource('ec2',region_name=region)
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
    ec2 = boto3.client('ec2',region_name=region)
    client = ec2.describe_security_groups()

    for i in client['SecurityGroups']:
        ec2res = boto3.resource('ec2',region_name=region)
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
    ec2 = boto3.client('ec2',region_name=region)
    client = ec2.describe_network_interfaces()

    for i in client['NetworkInterfaces']:
        ec2res = boto3.resource('ec2',region_name=region)
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
    ec2 = boto3.client('elb',region_name=region)
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
    ec2 = boto3.client('elbv2',region_name=region)
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

def apigatewaytagging():
    client = boto3.client('apigateway')
    for i in client.get_rest_apis()['items']:
        apiid = (i['id'])
        arnres = f'arn:aws:apigateway:{region}::/restapis/{apiid}'
        updatetags = client.tag_resource(
            resourceArn=arnres,
            tags={'Company' : 'AP', 'Country' : 'KR', 'Service' : '', 'STAGE' : 'ETC'}
        )

        print (updatetags)

def sagemakertagging():
    sage = boto3.client('sagemaker', region_name='ap-northeast-2')
    train = sage.list_training_jobs(MaxResults=100)
    for i in train['TrainingJobSummaries']:
        resarn = i['TrainingJobArn']
        tags = sage.add_tags(ResourceArn=resarn,Tags=[{'Key' : 'Country', 'Value' : 'KR'},{'Key' : 'Company', 'Value' : 'AP'},{'Key' : 'Sytem', 'Value' : 'DigitalRnD Recsys'},{'Key' : 'STAGE', 'Value' : 'PRD'}])
        print (resarn)
        time.sleep(1)

    while True:
        try:
            check = train['NextToken']
            train2 = sage.list_training_jobs(NextToken=check,MaxResults=100)
            for j in train2['TrainingJobSummaries']:
                resarn2 = j['TrainingJobArn']
                tags2 = sage.add_tags(ResourceArn=resarn2,Tags=[{'Key' : 'Country', 'Value' : 'KR'},{'Key' : 'Company', 'Value' : 'AP'},{'Key' : 'Sytem', 'Value' : 'DigitalRnD Recsys'},{'Key' : 'STAGE', 'Value' : 'PRD'}])
                print (resarn2)
                time.sleep(1)
        except KeyError:
            sys.exit()

def sagemakertagging2():
    sage = boto3.client('sagemaker', region_name='ap-northeast-2')
    train = sage.list_endpoint_configs(MaxResults=100)
    for i in train['EndpointConfigs']:
        resarn = i['EndpointConfigArn']
        tag = sage.add_tags(ResourceArn=resarn,Tags=[{'Key' : 'Country', 'Value' : 'KR'},{'Key' : 'Company', 'Value' : 'AP'},{'Key' : 'Sytem', 'Value' : 'DigitalRnD Recsys'},{'Key' : 'STAGE', 'Value' : 'PRD'}])
        print (resarn)
        time.sleep(1)

def InsTags(instanceid):
    ec2 = boto3.resource('ec2')
    
    for instance in ec2.instances.filter(InstanceIds=[instanceid]):
        try:
            InsTags = list(filter(lambda tag: tag['Key'] == 'System' or tag['Key'] == 'Company' or tag['Key'] == 'Country' or tag['Key'] == 'STAGE', instance.tags))
            return (InsTags)
        except KeyError:
            pass

def Volumecheck(response):
    ec2res = boto3.resource('ec2')

    for i in response['Volumes']:
        if i['State'] == 'in-use':
            # 사용중인 Volume 중에서 System Tag 가 없는 Volume 만 진행
            try:
                tagcheck = [a for a in i['Tags'] if a['Key'] == 'System']
            except KeyError:
                tagcheck = None
                continue
            
            if tagcheck:
                tagnames = None
                continue
            else:
                instanceid = [b['InstanceId'] for b in i['Attachments']]
                tagnames = InsTags(instanceid[0])

            if tagnames:
                ec2res.Volume(i['VolumeId']).create_tags(Tags=tagnames)
                print (f"{i['VolumeId']} 볼륨에 {tagnames} 추가 완료하였습니다.")    


def VolumeTagging():
    ec2 = boto3.client('ec2')
    response = ec2.describe_volumes(MaxResults=100)

    Volumecheck(response)

    while True:
        try:
            ntoken = response['NextToken']
            response = ec2.describe_volumes(MaxResults=100,NextToken=ntoken)
            Volumecheck(response)
        
        except KeyError:
            sys.exit()


def ENIcheck(response,clenv):
    ec2 = boto3.client('ec2')
    ec2res = boto3.resource('ec2')

    for i in response['NetworkInterfaces']:
        tagcheck = [a for a in i['TagSet'] if a['Key'] == 'System']
        if tagcheck:
            continue
        else:
            try:
                if i['Attachment']:
                    p = re.compile('[0-9]{12}')
                    tagname = None

                    if i['Attachment']['InstanceOwnerId'] == 'amazon-rds':
                        tagname = rdscheck(i['Groups'])
                        
                    elif i['Attachment']['InstanceOwnerId'] == 'amazon-elb':
                        tagname = elbcheck(i['Groups'])
                        if not tagname:
                            tagname = elbcheck2(i['Groups'])
                        else:
                            tagname = None
                            continue

                    elif p.match(i['Attachment']['InstanceOwnerId']):
                        tagname = InsTags(i['Attachment']['InstanceId'])
                    
                    if tagname:
                        tagging = ec2res.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=tagname)
                        print (f"{i['NetworkInterfaceId']} eni 태그 {tagname} 등록하였습니다.")

                    else:
                        tagname = "Resource-ENI " + clenv
                        tagging = ec2res.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tagname}])
                        print (f"{i['NetworkInterfaceId']} eni 태그 {tagname} 등록하였습니다.")

                else:
                    tagname = "Resource-ENI " + clenv
                    tagging = ec2res.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tagname}])
                    print (f"{i['NetworkInterfaceId']} eni 태그 {tagname} 등록하였습니다.")
               
            except KeyError:
                pass


def ENITagging(clenv):
    ec2 = boto3.client('ec2')
    ec2res = boto3.resource('ec2')
    response = ec2.describe_network_interfaces(MaxResults=100)

    ENIcheck(response,clenv)

    while True:
        try:
            ntoken = response['NextToken']
            response = ec2.describe_network_interfaces(MaxResults=100,NextToken=ntoken)
            ENIcheck(response,clenv)
        
        except KeyError:
            sys.exit()


def SnapshotTagging():
    ec2 = boto3.client('ec2')
    ec2res = boto3.resource('ec2')
    response = ec2.describe_snapshots(OwnerIds=['self'],MaxResults=500)
    tagcheckInsert(response)

    while True:
        try:
            ntoken = response['NextToken']
            response = ec2.describe_snapshots(OwnerIds=['self'],MaxResults=500,NextToken=ntoken)
            tagcheckInsert(response)

        except KeyError:
            sys.exit()




#def lambda_handler(event, context):

    #amitagcreate()
    #createSnapshotTag()
    #enitagcreate("APPRD")
    #sgtagging("APPRD")
    #rdssnapshot()

    ### System 기반 Tagging 사용
    #volumtagging()
    #securitytagging()
    #networktagging()
    #elbtagging()
    #elb2tagging()
    #apigatewaytagging()
    #sagemakertagging2()

